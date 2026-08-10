from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Pet, Doctor, EditRequest


TIME_CHOICES = [
    ("09:00", "09:00 AM"),
    ("09:30", "09:30 AM"),
    ("10:00", "10:00 AM"),
    ("10:30", "10:30 AM"),
    ("11:00", "11:00 AM"),
    ("11:30", "11:30 AM"),
    ("12:00", "12:00 PM"),
    ("12:30", "12:30 PM"),
    ("13:00", "01:00 PM"),
    ("13:30", "01:30 PM"),
    ("14:00", "02:00 PM"),
    ("14:30", "02:30 PM"),
    ("15:00", "03:00 PM"),
]

class PetForm(forms.ModelForm):

    doctor = forms.ModelChoiceField(
        queryset=Doctor.objects.all(),
        empty_label=_("Select Doctor"),
        label=_("Doctor")
    )

    appointment_time = forms.ChoiceField(
        choices=TIME_CHOICES,
        label=_("Appointment Time")
    )

    class Meta:
        model = Pet

        exclude = ['appointment_number', 'status']

        labels = {
            'name': _('Name'),
            'species': _('Animal Type'),
            'date_of_birth': _('Date of Birth'),
            'visit_date': _('Visit Date'),
            'visit_reason': _('Visit Reason'),
            'owner_name': _('Owner Name'),
            'owner_phone': _('Owner Phone'),
            'appointment_type': _('Appointment Type'),
            'priority': _('Priority'),
        }

        widgets = {
            'date_of_birth': forms.DateInput(
                attrs={'type': 'date'}
            ),

            'visit_date': forms.DateInput(
                attrs={'type': 'date'}
            ),
        }


class EditRequestForm(forms.ModelForm):

    class Meta:
        model = EditRequest

        fields = [
            'edit_type',
            'reason',
            'new_visit_date',
            'new_appointment_time',
            'new_doctor',
            'new_owner_phone',
            'new_visit_reason',
            'new_pet_name',
            'new_priority',
        ]

        widgets = {
            'edit_type': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),

            'reason': forms.Textarea(
                attrs={
                    'rows': 4,
                    'placeholder': _(
                        'Describe the requested change...'
                    ),
                    'class': 'form-control'
                }
            ),

            'new_visit_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),

            'new_appointment_time': forms.TimeInput(
                attrs={
                    'type': 'time',
                    'class': 'form-control'
                }
            ),

            'new_doctor': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'new_owner_phone': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'new_visit_reason': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'new_pet_name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'new_priority': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
        }

        labels = {
            'edit_type': _('Edit Type'),
            'reason': _('Description'),
            'new_visit_date': _('New Visit Date'),
            'new_appointment_time': _('New Appointment Time'),
            'new_doctor': _('New Doctor'),
            'new_owner_phone': _('New Owner Phone'),
            'new_visit_reason': _('New Visit Reason'),
            'new_pet_name': _('New Pet Name'),
            'new_priority': _('New Priority'),
        }