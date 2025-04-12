from django import forms
from .models import Booking
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from collections import defaultdict
from .constants import TABLE_INVENTORY

class BookingForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=User.objects.filter(is_staff=False),
        required=False,  # Optional for regular users (auto-assigned), required for staff
        label="Customer",
        help_text="Select a customer (only visible to staff)."
    )
    class Meta:
        model = Booking
        fields = ['user', 'date', 'time', 'num_guests', 'special_request', 'send_reminder']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # Capture request for role checks
        super().__init__(*args, **kwargs)

        if not self.request or not self.request.user.is_staff:
            self.fields.pop('user')  # Hide the field for regular users

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date and date < timezone.now().date():
            raise ValidationError("You can't book a table in the past.")
        return date

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')
        num_guests = cleaned_data.get('num_guests')

        if not date or not time or not num_guests:
            return cleaned_data  # Let field-level errors handle missing data

        # If editing and nothing has changed, skip re-validation
        if self.instance.pk:
            same_booking = (
                self.instance.date == date and
                self.instance.time == time and
                self.instance.num_guests == num_guests
            )
            if same_booking:
                return cleaned_data

        # Find best-fit table size
        suitable_sizes = sorted(size for size in TABLE_INVENTORY if size >= num_guests)
        if not suitable_sizes:
            raise ValidationError("Sorry, we can't accommodate that many guests.")

        best_fit_size = suitable_sizes[0]

        # Count how many tables of that size are already booked at this date/time
        existing_bookings = Booking.objects.filter(
            date=date,
            time=time,
            is_cancelled=False
        )

        # Exclude self when editing
        if self.instance.pk:
            existing_bookings = existing_bookings.exclude(pk=self.instance.pk)

        # Count how many best-fit tables are already taken
        taken = 0
        for booking in existing_bookings:
            for size in sorted(TABLE_INVENTORY):
                if size >= booking.num_guests:
                    if size == best_fit_size:
                        taken += 1
                    break

        if taken >= TABLE_INVENTORY[best_fit_size]:
            raise ValidationError("This time slot is fully booked for your party size. Please choose another.")

        return cleaned_data


class StaffBookingForm(BookingForm):
    user = forms.ModelChoiceField(
    queryset=User.objects.all(),
    label="Customer"
    )

    class Meta(BookingForm.Meta):
        fields = ['user'] + BookingForm.Meta.fields
