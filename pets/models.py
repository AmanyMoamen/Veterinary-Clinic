from django.db import models


class Doctor(models.Model):
    name = models.CharField(max_length=100)
    max_appointments_per_day = models.PositiveIntegerField(default=3)

    def __str__(self):
        return self.name


class Pet(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=50)

    date_of_birth = models.DateField(null=True, blank=True)

    visit_date = models.DateField(null=True, blank=True)

    visit_reason = models.CharField(
        max_length=200,
        blank=True,
        default=""
    )

    owner_name = models.CharField(max_length=100)
    owner_phone = models.CharField(max_length=15)
    appointment_type = models.CharField(max_length=20)

    PRIORITY_CHOICES = [
        ("Normal", "Normal"),
        ("Urgent", "Urgent"),
        ("Emergency", "Emergency"),
    ]

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default="Normal"
    )

    doctor = models.CharField(max_length=100)

    appointment_time = models.TimeField()

    def __str__(self):
        return self.name


class EditRequest(models.Model):
    EDIT_TYPE_CHOICES = [
        ("", "Select Edit Type"),
        ("Appointment Date", "Appointment Date"),
        ("Appointment Time", "Appointment Time"),
        ("Doctor", "Doctor"),
        ("Visit Reason", "Visit Reason"),
        ("Owner Phone", "Owner Phone"),
        ("Pet Name", "Pet Name"),
        ("Priority", "Priority"),
        ("Other", "Other"),
    ]    

    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)

    edit_type = models.CharField(
        max_length=50,
        choices=EDIT_TYPE_CHOICES,
        blank=False,
        default=""
    )   

    reason = models.TextField()

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pet.name} - {self.edit_type}"