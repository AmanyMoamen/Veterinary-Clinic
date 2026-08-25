from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import (
    Branch,
    Pet,
    Doctor,
    DoctorSchedule,
    EditRequest,
    UserProfile,
)

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    extra = 0

admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    inlines = [
        UserProfileInline,
    ]


# =========================
# Branch Admin
# =========================

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "address",
    )

    search_fields = (
        "name",
        "address",
    )


# =========================
# User Profile Admin
# =========================

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "role",
        "branch",
    )

    list_filter = (
        "role",
        "branch",
    )

    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
        "branch__name",
    )


# =========================
# Doctor Admin
# =========================

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "user",
        "branch",
        "consultation_time",
        "max_appointments_per_day",
    )

    list_filter = (
        "branch",
    )

    search_fields = (
        "name",
        "user__username",
    )


# =========================
# Doctor Schedule Admin
# =========================

@admin.register(DoctorSchedule)
class DoctorScheduleAdmin(admin.ModelAdmin):

    list_display = (
        "doctor",
        "branch",
        "date",
        "shift",
        "start_time",
        "end_time",
    )

    list_filter = (
        "branch",
        "shift",
        "date",
        "doctor",
    )

    search_fields = (
        "doctor__name",
        "branch__name",
    )

    ordering = (
        "date",
        "start_time",
    )


# =========================
# Pet Admin
# =========================

@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):

    list_display = (
        "appointment_number",
        "name",
        "branch",
        "doctor",
        "visit_date",
        "appointment_time",
        "priority",
        "status",
    )

    list_filter = (
        "branch",
        "priority",
        "status",
        "visit_date",
        "doctor",
    )

    search_fields = (
        "name",
        "owner_name",
        "owner_phone",
        "appointment_number",
        "doctor",
        "branch__name",
    )


# =========================
# Edit Request Admin
# =========================

@admin.register(EditRequest)
class EditRequestAdmin(admin.ModelAdmin):

    list_display = (
        "pet",
        "user",
        "edit_type",
        "reason",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "edit_type",
        "created_at",
    )

    search_fields = (
        "pet__name",
        "reason",
    )

    def save_model(self, request, obj, form, change):

        super().save_model(
            request,
            obj,
            form,
            change
        )

        # Apply requested change
        # only when Admin approves it

        if obj.status == "Approved":

            pet = obj.pet

            if (
                obj.edit_type == "Appointment Date"
                and obj.new_visit_date
            ):
                pet.visit_date = obj.new_visit_date

            elif (
                obj.edit_type == "Appointment Time"
                and obj.new_appointment_time
            ):
                pet.appointment_time = obj.new_appointment_time

            elif (
                obj.edit_type == "Doctor"
                and obj.new_doctor
            ):
                pet.doctor = obj.new_doctor

            elif (
                obj.edit_type == "Owner Phone"
                and obj.new_owner_phone
            ):
                pet.owner_phone = obj.new_owner_phone

            elif (
                obj.edit_type == "Visit Reason"
                and obj.new_visit_reason
            ):
                pet.visit_reason = obj.new_visit_reason

            elif (
                obj.edit_type == "Pet Name"
                and obj.new_pet_name
            ):
                pet.name = obj.new_pet_name

            elif (
                obj.edit_type == "Priority"
                and obj.new_priority
            ):
                pet.priority = obj.new_priority

            pet.save()