from django.db import models
from django.contrib.auth.models import User


# =========================
# Branch
# =========================

class Branch(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    address = models.CharField(
        max_length=200,
        blank=True
    )

    def __str__(self):
        return self.name


# =========================
# User Profile / Roles
# =========================

class UserProfile(models.Model):

    ROLE_CHOICES = [
        ("Admin", "Admin"),
        ("Receptionist", "Receptionist"),
        ("Doctor", "Doctor"),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="Receptionist"
    )

    branch = models.ForeignKey(
        Branch,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users"
    )

    def __str__(self):
        return f"{self.user.username} - {self.role}"


# =========================
# Doctor
# =========================

class Doctor(models.Model):

    name = models.CharField(
        max_length=100
    )

    # Link doctor to Django user account
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="doctor"
    )

    branch = models.ForeignKey(
        "Branch",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="doctors"
    )

    consultation_time = models.PositiveIntegerField(
        default=30,
        help_text="Consultation time in minutes"
    )

    max_appointments_per_day = models.PositiveIntegerField(
        default=3
    )

    def __str__(self):
        return self.name


# =========================
# Pet / Appointment
# =========================

class Pet(models.Model):

    name = models.CharField(
        max_length=100
    )

    species = models.CharField(
        max_length=50
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True
    )

    visit_date = models.DateField(
        null=True,
        blank=True
    )

    visit_reason = models.CharField(
        max_length=200,
        blank=True,
        default=""
    )

    owner_name = models.CharField(
        max_length=100
    )

    owner_phone = models.CharField(
        max_length=15
    )

    appointment_type = models.CharField(
        max_length=20
    )

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
   
    branch = models.ForeignKey(
        "Branch",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="appointments"
    )    

    STATUS_CHOICES = [
        ("Waiting", "Waiting"),
        ("Arrived", "Arrived"),
        ("Cancelled", "Cancelled"),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Waiting"
    )

    doctor = models.CharField(
        max_length=100
    )

    appointment_time = models.TimeField()

    # Appointment Serial Number
    appointment_number = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):

        if not self.appointment_number:

            last_pet = Pet.objects.order_by("-id").first()

            if last_pet and last_pet.appointment_number:

                try:
                    last_number = int(
                        last_pet.appointment_number.split("-")[1]
                    )

                except:
                    last_number = last_pet.id

            else:
                last_number = 0

            self.appointment_number = (
                f"APT-{last_number + 1:04d}"
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# =========================
# Edit Request
# =========================

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
    ]

    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="edit_requests"
    )

    edit_type = models.CharField(
        max_length=50,
        choices=EDIT_TYPE_CHOICES,
        blank=False,
        default=""
    )

    reason = models.TextField()

    new_visit_date = models.DateField(
        null=True,
        blank=True
    )

    new_appointment_time = models.TimeField(
        null=True,
        blank=True
    )

    new_doctor = models.CharField(
        max_length=100,
        blank=True
    )

    new_owner_phone = models.CharField(
        max_length=15,
        blank=True
    )

    new_visit_reason = models.CharField(
        max_length=200,
        blank=True
    )

    new_pet_name = models.CharField(
        max_length=100,
        blank=True
    )

    new_priority = models.CharField(
        max_length=20,
        choices=Pet.PRIORITY_CHOICES,
        blank=True,
        null=True
    )

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

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.pet.name} - {self.edit_type}"