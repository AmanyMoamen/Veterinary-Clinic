from django.contrib import admin
from .models import Pet, Doctor, EditRequest

admin.site.register(Pet)
admin.site.register(Doctor)
admin.site.register(EditRequest)