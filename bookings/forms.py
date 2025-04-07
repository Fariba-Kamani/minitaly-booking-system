from django import forms
from .models import Booking
from django.utils import timezone

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['date', 'time', 'num_guests', 'special_request', 'send_reminder']
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
        date = cleaned_data.get('date') or self.instance.date
        time = cleaned_data.get('time') or self.instance.time

        if self.instance.pk:
            if (
                self.instance.date == date and
                self.instance.time == time and
                self.instance.num_guests == cleaned_data.get('num_guests')
            ):
                return cleaned_data

        conflict_qs = Booking.objects.filter(date=date, time=time)
        if self.instance.pk:
            conflict_qs = conflict_qs.exclude(pk=self.instance.pk)

        if conflict_qs.exists():
            raise forms.ValidationError("This time slot is already booked. Please choose another.")

        return cleaned_data
