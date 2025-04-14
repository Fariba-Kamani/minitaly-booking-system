"""
staff/views.py

Defines views for staff/admin users to manage restaurant bookings.

All views are protected with `user_passes_test(lambda u: u.is_staff)`
to restrict access to staff users only.

Includes:
- Dashboard view with filtering
- Booking creation, update, and soft-delete functionality
- Email notifications to customers
"""

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


@method_decorator(user_passes_test(lambda u: u.is_staff), name='dispatch')
class BookingDashboardView(ListView):
    """
    Displays all upcoming, non-cancelled bookings for staff/admin users.

    Supports optional filtering via GET parameters:
    - date: Exact match (YYYY-MM-DD)
    - time: Exact match (HH:MM[:SS])
    - customer: Partial match on username
    """
    model = Booking
    template_name = 'staff/dashboard.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        queryset = Booking.objects.filter(
            date__gte=date.today(),
            is_cancelled=False
        ).order_by('date', 'time')

        # Optional filtering from query parameters
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
    Allows staff to update an existing booking without changing the customer.

    Uses a custom form (StaffBookingForm) that excludes the 'user' field,
    ensuring that the booking remains associated with the original customer.
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
        # Remove 'user' field to prevent changes to the customer
        form.fields.pop('user', None)
        return form

    def form_valid(self, form):
        # Enforce original customer assignment, even if tampering attempted
        form.instance.user = self.get_object().user
        staff_name = self.request.user.username
        messages.success(
                self.request,
                f"Booking updated successfully by staff: {staff_name}.")
        return super().form_valid(form)


@method_decorator(user_passes_test(lambda u: u.is_staff), name='dispatch')
class StaffBookingDeleteView(DeleteView):
    """
    Allows staff to cancel a booking (soft-delete approach).

    Instead of deleting the booking, it:
    - Sets `is_cancelled=True`
    - Records a cancellation reason
    - Sends an email to notify the customer

    GET requests are blocked to avoid accidental cancellations.
    """
    model = Booking
    success_url = reverse_lazy('staff_dashboard')
    template_name = 'staff/dashboard.html'

    def get(self, request, *args, **kwargs):
        # Block GET access — use POST only to prevent accidental deletions
        return redirect('staff_dashboard')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_cancelled = True
        self.object.cancellation_reason = request.POST.get(
            "cancellation_reason", "")
        self.object.save()

        # Send cancellation email to customer
        send_mail(
            subject='Your booking has been cancelled',
            message=(
                "Dear "
                + (
                    self.object.user.first_name
                    or self.object.user.username
                )
                + ",\n\n"
                "Your booking on "
                + f"{self.object.date} at "
                + f"{self.object.time.strftime('%H:%M')} "
                + "has been cancelled.\n"
                "Reason: "
                + (
                    f"{self.object.cancellation_reason}"
                    if self.object.cancellation_reason
                    else "No reason provided."
                )
                + "\n\n"
                "If this was a mistake, please contact the restaurant.\n\n"
                "Best regards,\nMinitaly"
            ),
            from_email=None,
            recipient_list=[self.object.user.email],
            fail_silently=False,
        )

        messages.success(
            request,
            "Booking cancelled successfully by staff: "
            f"{request.user.username}."
        )

        return redirect(self.success_url)


@method_decorator(user_passes_test(lambda u: u.is_staff), name='dispatch')
class StaffBookingCreateView(CreateView):
    """
    Allows staff to create a new booking on behalf of a customer.

    Features:
    - Staff selects customer from a dropdown (`user` field).
    - Sends confirmation email to the customer.
    - Displays staff attribution in the success message.
    """
    model = Booking
    form_class = StaffBookingForm
    template_name = 'staff/staff_form.html'
    success_url = reverse_lazy('staff_dashboard')

    def get_form_kwargs(self):
        # Pass request into form for potential custom logic
        # (ex., filtering customers)
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)

        # Send confirmation email to customer
        send_mail(
            subject="Your booking is confirmed - Minitaly",
            message=(
                "Dear "
                + (
                    form.instance.user.first_name
                    or form.instance.user.username
                )
                + ",\n\n"
                "A booking has been made for you by our staff:\n"
                f"Date: {form.instance.date}\n"
                f"Time: {form.instance.time.strftime('%H:%M')}\n"
                f"Guests: {form.instance.num_guests}\n\n"
                "To make changes, please log in or contact us.\n\n"
                "Best regards,\nMinitaly"
            ),
            from_email=None,
            recipient_list=[form.instance.user.email],
            fail_silently=False,
        )

        customer_name = form.cleaned_data['user'].username
        staff_name = self.request.user.username
        messages.success(
            self.request,
            (
                f"Booking created successfully for {customer_name} "
                f"by staff: {staff_name}."
            )
        )
        return response
