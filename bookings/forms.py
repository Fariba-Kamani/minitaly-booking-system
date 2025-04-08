from django import forms
from .models import Booking
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

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

        if not date or not time:
            return cleaned_data  # Let field-level errors handle missing values

        # Editing logic — skip conflict check if unchanged
        if self.instance.pk:
            same_booking = (
                self.instance.date == date and
                self.instance.time == time and
                self.instance.num_guests == num_guests
            )
            if same_booking:
                return cleaned_data

        # Conflict check
        conflicts = Booking.objects.filter(date=date, time=time, is_cancelled=False)
        if self.instance.pk:
            conflicts = conflicts.exclude(pk=self.instance.pk)

        if conflicts.exists():
            raise ValidationError("This time slot is already booked. Please choose another.")

        return cleaned_data


class StaffBookingForm(BookingForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), label="Customer")

    class Meta(BookingForm.Meta):
        fields = ['user'] + BookingForm.Meta.fields
