from django import forms
from .models import Booking
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from collections import defaultdict
from .constants import TABLE_INVENTORY

class BookingForm(forms.ModelForm):
    """
    Form for customers to create or edit a booking.

    - Automatically hides the `user` field for regular users.
    - Validates against past dates.
    - Prevents overbooking based on available tables using TABLE_INVENTORY.
    """

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
        """
        Dynamically removes the `user` field for non-staff users
        to prevent customers from assigning bookings to others.
        """
        self.request = kwargs.pop('request', None)  # Capture request for access control
        super().__init__(*args, **kwargs)

        if not self.request or not self.request.user.is_staff:
            self.fields.pop('user')

    def clean_date(self):
        """
        Prevents bookings in the past.
        """
        date = self.cleaned_data.get('date')
        if date and date < timezone.now().date():
            raise ValidationError("You can't book a table in the past.")
        return date

    def clean(self):
        """
        Custom form-level validation to prevent overbooking based on table inventory.

        - Ensures the requested number of guests can be seated.
        - Finds the smallest suitable table size for the group.
        - Blocks booking if all tables of that size are already in use at the requested time.
        """
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')
        num_guests = cleaned_data.get('num_guests')

        # Skip validation if required fields are missing
        if not date or not time or not num_guests:
            return cleaned_data

        # If editing and no key fields have changed, allow without re-checking
        if self.instance.pk:
            same_booking = (
                self.instance.date == date and
                self.instance.time == time and
                self.instance.num_guests == num_guests
            )
            if same_booking:
                return cleaned_data

        # Determine the smallest table size that fits this guest count
        suitable_sizes = sorted(size for size in TABLE_INVENTORY if size >= num_guests)
        if not suitable_sizes:
            raise ValidationError("Sorry, we can't accommodate that many guests.")

        best_fit_size = suitable_sizes[0]

        # Fetch bookings that conflict with this slot and are not cancelled
        existing_bookings = Booking.objects.filter(
            date=date,
            time=time,
            is_cancelled=False
        )

        # Exclude current booking instance when editing
        if self.instance.pk:
            existing_bookings = existing_bookings.exclude(pk=self.instance.pk)

        # Count how many best-fit tables are already in use
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
    """
    Inherits from BookingForm but exposes the `user` field to allow staff
    to create or edit bookings on behalf of any customer.
    """
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Customer"
    )

    class Meta(BookingForm.Meta):
        fields = ['user'] + BookingForm.Meta.fields
