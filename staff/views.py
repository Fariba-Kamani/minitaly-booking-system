from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from bookings.models import Booking
from datetime import date

# Admin check
@method_decorator(user_passes_test(lambda u: u.is_staff), name='dispatch')
class BookingDashboardView(ListView):
    model = Booking
    template_name = 'staff/dashboard.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        return Booking.objects.filter(date__gte=date.today()).order_by('date', 'time')
