from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from bookings.models import Booking
from datetime import timedelta

class Command(BaseCommand):
    help = 'Sends reminder emails for bookings happening in 24 hours'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        print(f"Now: {now}")
        reminder_time = now + timedelta(days=1)
        reminder_date = reminder_time.date()
        reminder_hour = reminder_time.time().replace(minute=0, second=0, microsecond=0)

        print(f"Reminder time target: {reminder_time}")
        print(f"Reminder date: {reminder_date}")
        print(f"Reminder hour: {reminder_hour}")

        bookings = Booking.objects.filter(
            date=reminder_date,
            time__hour=reminder_hour.hour,
            send_reminder=True,
            reminder_sent=False,
            is_cancelled=False
        )
        print(f"Found bookings: {bookings.count()}")
        for booking in bookings:
            print(f"Booking: {booking.user.username}, {booking.date} at {booking.time}, reminder={booking.send_reminder}, cancelled={booking.is_cancelled}")
            user = booking.user
            email = user.email

            table_numbers = ", ".join([str(t.number) for t in booking.tables.all()]) or "assigned at arrival"

            send_mail(
                subject="Reminder: Your Minitaly booking is tomorrow!",
                message=f"Dear {user.first_name or user.username},\n\n"
                        f"This is a reminder about your booking at Minitaly:\n"
                        f"Date: {booking.date}\n"
                        f"Time: {booking.time.strftime('%H:%M')}\n"
                        f"Guests: {booking.num_guests}\n"
                        f"Table(s): {table_numbers}\n\n"
                        f"We look forward to seeing you!\n\n"
                        f"Best regards,\nMinitaly",
                from_email=None,
                recipient_list=[email],
                fail_silently=False,
            )
            # Mark the reminder as sent to avoid duplicates
            booking.reminder_sent = True
            booking.save()

        self.stdout.write(self.style.SUCCESS(f"Sent {bookings.count()} reminder(s)."))