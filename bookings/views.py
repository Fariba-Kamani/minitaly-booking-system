from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin as registered_users_only
from django.utils import timezone
from .models import Booking
from .forms import BookingForm

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
    
    
class BookingCreateView(registered_users_only, generic.CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'bookings/booking_form.html'
    success_url = reverse_lazy('booking_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
