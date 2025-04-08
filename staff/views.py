from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic import ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from django.core.mail import send_mail
from datetime import date

from bookings.models import Booking
from bookings.forms import BookingForm

# Admin check
@method_decorator(user_passes_test(lambda u: u.is_staff), name='dispatch')
class BookingDashboardView(ListView):
    model = Booking
    template_name = 'staff/dashboard.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        queryset = Booking.objects.filter(
        date__gte=date.today(),
        is_cancelled=False  # exclude cancelled bookings
        ).order_by('date', 'time')

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
    model = Booking
    form_class = BookingForm
    template_name = 'staff/staff_form.html'
    success_url = reverse_lazy('staff_dashboard')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request  # pass the request into the form
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.get_object().user
        staff_name = self.request.user.username
        messages.success(self.request, f"Booking updated successfully by staff: {staff_name}.")
        return super().form_valid(form)


@method_decorator(user_passes_test(lambda u: u.is_staff), name='dispatch')
class StaffBookingDeleteView(DeleteView):
    model = Booking
    success_url = reverse_lazy('staff_dashboard')
    template_name = 'staff/dashboard.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_cancelled = True
        self.object.cancellation_reason = request.POST.get("cancellation_reason", "")
        self.object.save()

        # Send email
        send_mail(
            subject='Your booking has been cancelled',
            message=f"Dear {self.object.user.first_name or self.object.user.username},\n\n"
                    f"Your booking on {self.object.date} at {self.object.time.strftime('%H:%M')} has been cancelled.\n"
                    f"Reason: {self.object.cancellation_reason or 'No reason provided.'}\n\n"
                    f"If this was a mistake, please contact the restaurant.\n\n"
                    f"Best regards,\nMinitaly",
            from_email=None,  # Uses DEFAULT_FROM_EMAIL
            recipient_list=[self.object.user.email],
            fail_silently=False,
        )

        messages.success(
            request,
            f"Booking cancelled successfully by staff: {request.user.username}."
        )
        return redirect(self.success_url)
