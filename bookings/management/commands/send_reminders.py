"""
Custom management command to send reminder emails to customers
24 hours before their restaurant booking at Minitaly.

Reminders are only sent if:
- The booking is not cancelled
- The user has opted in to reminders
- A reminder has not already been sent (tracked via `reminder_sent`)
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from bookings.models import Booking
from datetime import timedelta


class Command(BaseCommand):
    """
    Django custom command to send upcoming booking reminders.

    Run with:
        python manage.py send_reminders

    Use this with a cron scheduler (e.g. django-cron) for automation.
    """
    help = 'Sends reminder emails for bookings happening in 24 hours'

    def handle(self, *args, **kwargs):
        now = timezone.now()

        # Calculate the exact time 24 hours from now
        reminder_time = now + timedelta(days=1)

        # Extract target date and hour (rounded to the hour)
        reminder_date = reminder_time.date()
        reminder_hour = reminder_time.time().replace(minute=0, second=0, microsecond=0)

        # Query bookings that match the reminder window
        bookings = Booking.objects.filter(
            date=reminder_date,
            time__hour=reminder_hour.hour,
            send_reminder=True,
            reminder_sent=False,
            is_cancelled=False
        )

        for booking in bookings:
            user = booking.user
            email = user.email

            # Get assigned table numbers or fall back to a placeholder
            table_numbers = ", ".join([str(t.number) for t in booking.tables.all()]) or "assigned at arrival"

            # Construct and send reminder email
            send_mail(
                subject="Reminder: Your Minitaly booking is tomorrow!",
                message=(
                    f"Dear {user.first_name or user.username},\n\n"
                    f"This is a reminder about your booking at Minitaly:\n"
                    f"Date: {booking.date}\n"
                    f"Time: {booking.time.strftime('%H:%M')}\n"
                    f"Guests: {booking.num_guests}\n"
                    f"Table(s): {table_numbers}\n\n"
                    f"We look forward to seeing you!\n\n"
                    f"Best regards,\nMinitaly"
                ),
                from_email=None,  # Uses DEFAULT_FROM_EMAIL
                recipient_list=[email],
                fail_silently=False,
            )

            # Mark reminder as sent to avoid duplicate emails
            booking.reminder_sent = True
            booking.save()

        # Output result to terminal
        self.stdout.write(self.style.SUCCESS(f"Sent {bookings.count()} reminder(s)."))
