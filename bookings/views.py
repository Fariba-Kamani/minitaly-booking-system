from datetime import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils import timezone
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_GET

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
            date__gte=now, # __gte = Django field look up; greater than or equal to
            is_cancelled=False
        ).order_by('date', 'time')

        # Filter for past bookings using date less than today
        context['past_bookings'] = queryset.filter(
            date__lt=now # __lt = Django field look up; less than
        ).order_by('-date', '-time')

        return context


@method_decorator(login_required, name='dispatch')
class BookingUpdateView(UpdateView):
    """
    View for updating a booking by a logged-in customer.
    - Only the booking's owner can access and update it.
    - Unauthorized access is blocked with an HTTP 403 Forbidden response.
    """
    model = Booking
    form_class = BookingForm
    template_name = 'bookings/booking_form.html'
    success_url = reverse_lazy('booking_list')

    def get_queryset(self):
        # Only return bookings belonging to the logged-in user
        return Booking.objects.filter(user=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        # Defensive check: ensure the user owns this booking
        booking = get_object_or_404(Booking, pk=kwargs['pk'])
        if booking.user != request.user:
            return HttpResponseForbidden("You are not allowed to edit this booking.")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Your booking has been successfully updated!")
        return super().form_valid(form)
    

@method_decorator(login_required, name='dispatch')
class BookingDeleteView(SuccessMessageMixin, DeleteView):
    """
    View for canceling a booking by the booking owner.
    - Only the user who made the booking can cancel it.
    - Displays a success message upon cancellation.
    - Sends a cancellation email instead of deleting the booking.
    """
    model = Booking
    template_name = 'bookings/booking_confirm_delete.html'
    success_url = reverse_lazy('booking_list')
    success_message = "Your booking has been cancelled."

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        booking = get_object_or_404(Booking, pk=kwargs['pk'])
        if booking.user != request.user:
            return HttpResponseForbidden("You are not allowed to cancel this booking.")
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        booking = self.get_object()
        booking.is_cancelled = True
        booking.save()

        # Send cancellation email
        send_mail(
            subject="Your booking has been cancelled - Minitaly",
            message=f"Dear {booking.user.first_name or booking.user.username},\n\n"
                    f"Your booking on {booking.date} at {booking.time.strftime('%H:%M')} has been cancelled.\n\n"
                    f"If this was a mistake, please contact us to rebook.\n\n"
                    f"Best regards,\nMinitaly",
            from_email=None,
            recipient_list=[booking.user.email],
            fail_silently=False,
        )

        messages.success(request, self.success_message)
        return redirect(self.success_url)


@method_decorator(login_required, name='dispatch')
class BookingCreateView(CreateView):
    """
    View for creating a new booking by a logged-in customer.
    - Automatically assigns the logged-in user as the booking owner.
    - Sends a confirmation email upon successful booking.
    - Displays a success message and redirects to the booking list.
    """
    model = Booking
    form_class = BookingForm
    template_name = 'bookings/booking_form.html'
    success_url = reverse_lazy('booking_list')

    def form_valid(self, form):
        # Associate the booking with the current user
        form.instance.user = self.request.user
        response = super().form_valid(form)

        # Send confirmation email to user
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
            from_email=None,  # Uses DEFAULT_FROM_EMAIL
            recipient_list=[self.request.user.email],
            fail_silently=False,
        )

        # Show success message and proceed
        messages.success(self.request, "Your booking has been successfully created!")
        return response


@require_GET
@login_required
def available_slots_api(request):
    """
    API endpoint to fetch available booking time slots
    for a given date (string) and guest count (integer).
    - Only accessible by logged-in users.
    - Returns a JSON response with available time slots from custom utility function.
    """
    date_str = request.GET.get('date')
    guests = request.GET.get('guests')

    # Check for required query parameters in GET request
    if not date_str or not guests:
        return JsonResponse({'error': 'Missing parameters'}, status=400)

    try:
        # Validate date and guest input
        selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        guests = int(guests)
    except ValueError:
        return JsonResponse({'error': 'Invalid input'}, status=400)

    # Get available slots from utility function
    slots = get_available_time_slots(selected_date, guests)

    return JsonResponse({'slots': slots})
