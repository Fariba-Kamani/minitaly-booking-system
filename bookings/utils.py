"""
utils.py

Contains utility functions used across the booking system.

Includes:
- Time slot generation based on operating hours
- Availability logic for checking open time slots
- Email helper for sending cancellation notices
"""

from datetime import datetime, timedelta
from collections import defaultdict
from django.core.mail import send_mail
from django.conf import settings
from .constants import OPERATING_HOURS, TABLE_INVENTORY, MAX_GUESTS_PER_BOOKING
from .models import Booking


def generate_time_slots(date: datetime.date):
    """
    Generates all available time slots for a given date based on
    restaurant operating hours and interval settings.

    Args:
        date (datetime.date): The date for which to generate slots.

    Returns:
        list of datetime.time: All valid time slots for that day.
    """
    slots = []
    current = datetime.combine(date, OPERATING_HOURS['start'])
    end_time = datetime.combine(date, OPERATING_HOURS['end'])

    while current <= end_time:
        slots.append(current.time())
        current += OPERATING_HOURS['interval']
    
    return slots


def get_available_time_slots(date, num_guests):
    """
    Returns a list of time slots and their availability for a given date and group size.

    This function:
    - Finds the best-fit table size for the requested number of guests.
    - Tracks how many of those tables are already booked at each time.
    - Marks slots as available if at least one matching table is still free.

    Args:
        date (datetime.date): The selected date to check availability.
        num_guests (int): Number of guests in the booking request.

    Returns:
        list of dict: Each dict contains a time and a boolean indicating availability.
                      e.g. [{'time': 17:00, 'available': True}, ...]
    """
    all_slots = generate_time_slots(date)
    bookings = Booking.objects.filter(date=date)

    # Tracks how many tables are booked at each time slot by table size
    # Example: {17:00: {4: 2}} means 2 tables for 4 guests are taken at 17:00
    booked = defaultdict(lambda: defaultdict(int))

    for b in bookings:
        for size in sorted(TABLE_INVENTORY):
            if size >= b.num_guests:
                booked[b.time][size] += 1
                break

    available_slots = []

    for slot in all_slots:
        # Determine the best-fitting table size for this guest count
        suitable_sizes = sorted(size for size in TABLE_INVENTORY if size >= num_guests)

        if not suitable_sizes:
            available = False  # No suitable table exists
        else:
            best_fit = suitable_sizes[0]
            # Check if the number of booked tables is less than what's available
            available = booked[slot][best_fit] < TABLE_INVENTORY[best_fit]

        available_slots.append({
            "time": slot,
            "available": available
        })

    return available_slots


def send_cancellation_email(booking):
    """
    Sends an email to the customer confirming that their booking has been cancelled.

    Args:
        booking (Booking): The cancelled booking instance.
    """
    subject = "Your Booking Has Been Cancelled"

    message = (
        f"Dear {booking.user.first_name or booking.user.username},\n\n"
        f"Your booking on {booking.date} at {booking.time} has been cancelled.\n"
    )

    if booking.cancellation_reason:
        message += f"\nReason: {booking.cancellation_reason}\n"

    message += "\nThank you for understanding.\nMinitaly Team"

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[booking.user.email],
        fail_silently=False,
    )
