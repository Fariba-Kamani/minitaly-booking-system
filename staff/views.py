from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from bookings.models import Booking
from datetime import date
from django.db.models import Q

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
