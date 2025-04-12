"""
models.py

Defines the database models for the restaurant booking system.

Includes:
- Table model for seating arrangements
- Booking model for customer reservations
"""

from django.db import models
from django.contrib.auth.models import User


class Table(models.Model):
    """
    Represents a physical table in the restaurant.

    Attributes:
        number (int): Unique identifier for each table.
        capacity (int): Number of guests the table can accommodate.
    """
    number = models.PositiveIntegerField(unique=True)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return f"Table {self.number} (seats {self.capacity})"


class Booking(models.Model):
    """
    Represents a customer's booking/reservation.

    Attributes:
        user (User): The customer who made the booking.
        tables (ManyToMany[Table]): The tables assigned to the booking.
        date (DateField): The date of the booking.
        time (TimeField): The time of the booking.
        num_guests (int): The number of guests in the booking.
        special_request (str): Optional note from the customer.
        is_cancelled (bool): Whether the booking has been cancelled.
        cancellation_reason (str): Optional reason for cancellation.
        send_reminder (bool): Whether the user wants a reminder email.
        reminder_sent (bool): Prevents duplicate reminder emails.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    tables = models.ManyToManyField(Table)
    date = models.DateField()
    time = models.TimeField()
    num_guests = models.PositiveIntegerField()
    special_request = models.TextField(blank=True, null=True)
    is_cancelled = models.BooleanField(default=False)
    cancellation_reason = models.TextField(blank=True, null=True)
    send_reminder = models.BooleanField(default=True)
    reminder_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s booking on {self.date} at {self.time}"
