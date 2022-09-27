from django import forms
from django.forms import ValidationError, SelectDateWidget
from .models import *
import datetime


class AddRoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ("name", "capacity", "projector_availability")
        labels = {
            'name': 'Room name',
            'capacity': 'Room capacity',
            'projector_availability': 'Projector availability',
        }


class ModifyRoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ("name", "capacity", "projector_availability")


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ('date', 'comment',)
        labels = {
            'date': 'Booking date',
            'comment': 'Comment',
        }
        widgets = {
            'date': SelectDateWidget,
        }

    def clean(self):
        cleaned_data = super().clean()
        reservation_date = cleaned_data.get('date')
        # booking for past date -> validation
        today = datetime.date.today()
        if reservation_date < today:
            raise ValidationError('Booking for past date is not allowed!')
        # checking if room is already booked for chosen day
        already_reserved = list(self.instance.room.reservations.filter(date=reservation_date))
        if len(already_reserved) > 0:
            raise ValidationError(f"Room is already booked on {reservation_date}")


class DetailForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'capacity', 'projector_availability']
