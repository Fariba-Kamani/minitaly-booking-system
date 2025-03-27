from django.shortcuts import render
from .models import Booking

def my_bookings(request):
    bookings = Booking.objects.all().order_by('-date', '-time')  # Show most recent first
    return render(request, 'bookings/booking_list.html', {'bookings': bookings})
