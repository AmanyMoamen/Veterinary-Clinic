from django import forms
from .models import Pet


class PetForm(forms.ModelForm):

    class Meta:
        model = Pet
        fields = '__all__'

        widgets = {
            'visit_date': forms.DateInput(attrs={'type': 'date'}),
            'appointment_time': forms.TimeInput(attrs={'type': 'time'}),
        }