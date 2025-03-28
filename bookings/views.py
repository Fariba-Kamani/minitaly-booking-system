from django.shortcuts import render
from django.views import generic
from .models import Booking

class BookingListView(generic.ListView):
    model = Booking
    template_name = 'bookings/booking_list.html'
    context_object_name = 'bookings'
    ordering = ['-date', '-time']
