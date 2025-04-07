from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin as registered_users_only
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
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
        queryset = Booking.objects.filter(date__gte=date.today()).order_by('date', 'time')

        # Get query parameters
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

    def form_valid(self, form):
        staff_name = self.request.user.username  # define it first
        messages.success(self.request, f"Booking updated successfully by staff: {staff_name}.")
        return super().form_valid(form)


@method_decorator(user_passes_test(lambda u: u.is_staff), name='dispatch')
class StaffBookingDeleteView(SuccessMessageMixin, registered_users_only, DeleteView):
    model = Booking
    success_url = reverse_lazy('staff_dashboard')
    template_name = 'staff/dashboard.html'  # Not used, modal

    success_message = "Booking cancelled successfully by staff: %(username)s."

    def get_success_message(self, cleaned_data):
        return self.success_message % {'username': self.request.user.username}
