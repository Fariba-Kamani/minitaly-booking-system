from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin as registered_users_only
from django.utils import timezone
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import UpdateView, DeleteView
from django.http import JsonResponse
from .models import Booking
from .forms import BookingForm
from .utils import get_available_time_slots

def home(request):
    return render(request, 'index.html')

class BookingListView(generic.ListView):
    model = Booking
    template_name = 'bookings/booking_list.html'
    context_object_name = 'bookings'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now().date()

        context['upcoming_bookings'] = Booking.objects.filter(
            user=self.request.user,
            date__gte=now
        ).order_by('date', 'time')

        context['past_bookings'] = Booking.objects.filter(
            user=self.request.user,
            date__lt=now
        ).order_by('-date', '-time')

        return context
    

class BookingUpdateView(registered_users_only, UpdateView):
    model = Booking
    form_class = BookingForm
    template_name = 'bookings/booking_form.html'
    success_url = reverse_lazy('booking_list')

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, "Your booking has been successfully updated!")
        return super().form_valid(form)
    

class BookingDeleteView(SuccessMessageMixin, registered_users_only, DeleteView):
    model = Booking
    template_name = 'bookings/booking_confirm_delete.html'
    success_url = reverse_lazy('booking_list')
    success_message = "Your booking has been cancelled."

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

class BookingCreateView(registered_users_only, generic.CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'bookings/booking_form.html'
    success_url = reverse_lazy('booking_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Your booking has been successfully created!")
        return super().form_valid(form)


def available_slots_api(request):
    date_str = request.GET.get('date')
    guests = request.GET.get('guests')

    if not date_str or not guests:
        return JsonResponse({'error': 'Missing parameters'}, status=400)

    from datetime import datetime
    try:
        selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        guests = int(guests)
    except ValueError:
        return JsonResponse({'error': 'Invalid input'}, status=400)

    slots = get_available_time_slots(selected_date, guests)

    return JsonResponse({'slots': slots})
