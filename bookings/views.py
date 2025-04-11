from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin as registered_users_only
from django.utils import timezone
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import UpdateView, DeleteView
from django.http import JsonResponse
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Booking
from .forms import BookingForm
from .utils import get_available_time_slots

def home(request):
    return render(request, 'index.html')

# dispatch() is the first method called when a request reaches a class-based view,
# applying login_required to it ensures that the user must be logged in 
# before any other HTTP request is processed.
@method_decorator(login_required, name='dispatch')
class BookingListView(generic.ListView):
    """
    Displays the logged-in user's bookings.

    - Uses `get_queryset` to restrict the displayed bookings to the current user.
    - Separates upcoming and past bookings in the context data.
    - Requires user authentication to access this view.
    - Prevents access to other users' bookings even if URL tampering is attempted.
    """
    model = Booking
    template_name = 'bookings/booking_list.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        # Only return bookings for the currently logged-in user
        return Booking.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now().date()

        queryset = self.get_queryset()

        # Filter for future or today's bookings using date greater than or equal to today
        context['upcoming_bookings'] = queryset.filter(
            date__gte=now # __gte = Django field look up; greater than or equal to
        ).order_by('date', 'time')

        # Filter for past bookings using date less than today
        context['past_bookings'] = queryset.filter(
            date__lt=now # __lt = Django field look up; less than
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
        response = super().form_valid(form)

        # Send confirmation email
        send_mail(
            subject="Your booking is confirmed - Minitaly",
            message=f"Dear {self.request.user.first_name or self.request.user.username},\n\n"
                    f"Thank you for booking with Minitaly!\n\n"
                    f"Here are your booking details:\n"
                    f"Date: {form.instance.date}\n"
                    f"Time: {form.instance.time.strftime('%H:%M')}\n"
                    f"Guests: {form.instance.num_guests}\n"
                    f"Special Request: {form.instance.special_request or 'None'}\n\n"
                    f"We look forward to seeing you!\n\n"
                    f"Best regards,\nMinitaly",
            from_email=None,
            recipient_list=[self.request.user.email],
            fail_silently=False,
        )

        messages.success(self.request, "Your booking has been successfully created!")
        return response


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
