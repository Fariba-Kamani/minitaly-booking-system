from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Table(models.Model):
    number = models.PositiveIntegerField(unique=True)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return f"Table {self.number} (seats {self.capacity})"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    tables = models.ManyToManyField(Table)
    date = models.DateField()
    time = models.TimeField()
    num_guests = models.PositiveIntegerField()
    special_request = models.TextField(blank=True, null=True)
    is_cancelled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s booking on {self.date} at {self.time}"
