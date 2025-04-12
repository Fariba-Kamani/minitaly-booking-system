from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic import ListView, UpdateView, DeleteView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from django.core.mail import send_mail
from datetime import date

from bookings.models import Booking
from bookings.forms import BookingForm, StaffBookingForm

# --------------------------------------
# STAFF VIEWS - Protected by is_staff check
# --------------------------------------

@method_decorator(user_passes_test(lambda u: u.is_staff), name='dispatch')
class BookingDashboardView(ListView):
    """
    Displays all upcoming, non-cancelled bookings for staff/admin users.
    Supports filtering by date, time, and customer username via GET parameters.
    """
    model = Booking
    template_name = 'staff/dashboard.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        queryset = Booking.objects.filter(
            date__gte=date.today(),
            is_cancelled=False
        ).order_by('date', 'time')

        # Optional filters from query params
        selected_date = self.request.GET.get('date')
        selected_time = self.request.GET.get('time')
        customer = self.request.GET.get('customer')

        if selected_date:
            queryset = queryset.filter(date=selected_date)
        if selected_time:
            queryset = queryset.filter(time=selected_time)
        if customer:
            queryset = queryset.filter(user__username__icontains=customer)

        return queryset


@method_decorator(user_passes_test(lambda u: u.is_staff), name='dispatch')
class StaffBookingUpdateView(UpdateView):
    """
    Allows staff to update an existing booking while preserving customer assignment.
    Uses a custom form that excludes the 'user' field.
    """
    model = Booking
    form_class = StaffBookingForm
    template_name = 'staff/staff_form.html'
    success_url = reverse_lazy('staff_dashboard')

    def get_form_kwargs(self):
        # Pass request into form in case it's needed (e.g., for dynamic fields)
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Prevent staff from changing the customer during update
        form.fields.pop('user', None)
        return form

    def form_valid(self, form):
        # Enforce customer lock for security, in case of form tampering
        form.instance.user = self.get_object().user
        staff_name = self.request.user.username
        messages.success(self.request, f"Booking updated successfully by staff: {staff_name}.")
        return super().form_valid(form)


@method_decorator(user_passes_test(lambda u: u.is_staff), name='dispatch')
class StaffBookingDeleteView(DeleteView):
    """
    Allows staff to cancel a booking (soft-delete).
    - Marks the booking as is_cancelled=True
    - Captures a cancellation reason
    - Sends a cancellation email to the customer
    - Prevents GET access to avoid accidental deletions
    """
    model = Booking
    success_url = reverse_lazy('staff_dashboard')
    template_name = 'staff/dashboard.html'

    def get(self, request, *args, **kwargs):
        # Block GET access to this view — cancellations should only be via POST
        return redirect('staff_dashboard')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_cancelled = True
        self.object.cancellation_reason = request.POST.get("cancellation_reason", "")
        self.object.save()

        # Notify customer via email
        send_mail(
            subject='Your booking has been cancelled',
            message=f"Dear {self.object.user.first_name or self.object.user.username},\n\n"
                    f"Your booking on {self.object.date} at {self.object.time.strftime('%H:%M')} has been cancelled.\n"
                    f"Reason: {self.object.cancellation_reason or 'No reason provided.'}\n\n"
                    f"If this was a mistake, please contact the restaurant.\n\n"
                    f"Best regards,\nMinitaly",
            from_email=None,
            recipient_list=[self.object.user.email],
            fail_silently=False,
        )

        messages.success(
            request,
            f"Booking cancelled successfully by staff: {request.user.username}."
        )
        return redirect(self.success_url)


@method_decorator(user_passes_test(lambda u: u.is_staff), name='dispatch')
class StaffBookingCreateView(CreateView):
    """
    Allows staff to create a new booking on behalf of a customer.
    - Customer is selected from a dropdown
    - Sends confirmation email to the customer
    - Displays staff attribution in success message
    """
    model = Booking
    form_class = StaffBookingForm
    template_name = 'staff/staff_form.html'
    success_url = reverse_lazy('staff_dashboard')

    def get_form_kwargs(self):
        # Pass request into form if needed (e.g., for filtering users)
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)

        # Send confirmation email to the customer
        send_mail(
            subject="Your booking is confirmed - Minitaly",
            message=f"Dear {form.instance.user.first_name or form.instance.user.username},\n\n"
                    f"A booking has been made for you by our staff:\n"
                    f"Date: {form.instance.date}\n"
                    f"Time: {form.instance.time.strftime('%H:%M')}\n"
                    f"Guests: {form.instance.num_guests}\n\n"
                    f"If you need to make changes, please log in or contact us.\n\n"
                    f"Best regards,\nMinitaly",
            from_email=None,
            recipient_list=[form.instance.user.email],
            fail_silently=False,
        )

        customer_name = form.cleaned_data['user'].username
        staff_name = self.request.user.username
        messages.success(self.request, f"Booking created successfully for {customer_name} by staff: {staff_name}.")
        return response
