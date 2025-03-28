from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin as registered_users_only
from .models import Booking
from .forms import BookingForm

class BookingListView(generic.ListView):
    model = Booking
    template_name = 'bookings/booking_list.html'
    context_object_name = 'bookings'
    ordering = ['-date', '-time']

class BookingCreateView(registered_users_only, generic.CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'bookings/booking_form.html'
    success_url = reverse_lazy('booking_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
