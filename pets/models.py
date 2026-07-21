from django.db import models

class Pet(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=50)
    age = models.IntegerField()
    visit_date = models.DateField()

    owner_name = models.CharField(max_length=100)
    owner_phone = models.CharField(max_length=15)
    appointment_type = models.CharField(max_length=20)
    doctor = models.CharField(max_length=100)
    appointment_time = models.TimeField()

    def __str__(self):
        return self.name