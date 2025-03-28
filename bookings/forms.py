from django import forms
from .models import Booking
from django.utils import timezone

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['date', 'time', 'num_guests', 'special_request']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }
    
    def prevent_past_dates(self):
        date = self.cleaned_data['date']
        if date < timezone.now().date():
            raise forms.ValidationError("You can't book a table in the past.")
        return date
    # Django expects the method to be called `clean_<fieldname>`
    clean_date = prevent_past_dates

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')
        if date and time:
            conflicting_bookings = Booking.objects.filter(
                date=date,
                time=time,
                is_cancelled=False
            )
            if conflicting_bookings.exists():
                raise forms.ValidationError(
                    "Sorry, we already have a booking at this date and time. Please choose another slot."
                )
        return cleaned_data