from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
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
        staff_name = self.request.user.username  # ✅ define it first
        messages.success(self.request, f"Booking updated successfully by staff: {staff_name}.")
        return super().form_valid(form)


@method_decorator(user_passes_test(lambda u: u.is_staff), name='dispatch')
class StaffBookingDeleteView(DeleteView):
    model = Booking
    template_name = 'staff/staff_confirm_delete.html'
    success_url = reverse_lazy('staff_dashboard')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Booking cancelled successfully (by staff).")
        return super().delete(request, *args, **kwargs)
