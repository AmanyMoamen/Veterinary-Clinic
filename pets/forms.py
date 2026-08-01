from django import forms
from .models import Pet, Doctor, EditRequest


class PetForm(forms.ModelForm):

    doctor = forms.ModelChoiceField(
        queryset=Doctor.objects.all(),
        empty_label="Select Doctor"
    )

    class Meta:
        model = Pet

        exclude = ['appointment_number']

        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'visit_date': forms.DateInput(attrs={'type': 'date'}),
            'appointment_time': forms.TimeInput(attrs={'type': 'time'}),
        }


class EditRequestForm(forms.ModelForm):
    class Meta:
        model = EditRequest
        fields = ['edit_type', 'reason']

        widgets = {
            'edit_type': forms.Select(attrs={
                'class': 'form-control'
            }),

            'reason': forms.Textarea(attrs={
                'rows': 6,
                'placeholder': 'Describe the requested change in detail...',
                'class': 'form-control'
            }),
        }

        labels = {
            'edit_type': 'Edit Type',
            'reason': 'Description',
        }