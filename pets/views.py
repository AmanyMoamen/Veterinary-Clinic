from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Q
from datetime import datetime, timedelta, date

from .models import Pet, EditRequest, Doctor
from .forms import PetForm, EditRequestForm


def pet_list(request):
    pets = Pet.objects.all()
    doctors = Doctor.objects.all()

    filter_type = request.GET.get("filter")
    doctor = request.GET.get("doctor")

    if filter_type == "today":
        pets = pets.filter(visit_date=date.today())

    elif filter_type == "week":
        today = date.today()
        end_week = today + timedelta(days=7)
        pets = pets.filter(
            visit_date__gte=today,
            visit_date__lte=end_week
        )

    elif filter_type == "normal":
        pets = pets.filter(priority="Normal")

    elif filter_type == "urgent":
        pets = pets.filter(priority="Urgent")

    elif filter_type == "emergency":
        pets = pets.filter(priority="Emergency")

    if doctor:
        pets = pets.filter(doctor=doctor)

    return render(
        request,
        "pets/index.html",
        {
            "pets": pets,
            "doctors": doctors,
        },
    )


def add_pet(request):
    if request.method == "POST":
        form = PetForm(request.POST)

        if form.is_valid():
            doctor = form.cleaned_data["doctor"]
            visit_date = form.cleaned_data["visit_date"]
            appointment_time = form.cleaned_data["appointment_time"]

            appointments_count = Pet.objects.filter(
                doctor=doctor,
                visit_date=visit_date
            ).count()

            if appointments_count >= doctor.max_appointments_per_day:
                return render(
                    request,
                    "pets/add_pet.html",
                    {
                        "form": form,
                        "error": "This doctor already has the maximum number of appointments for this day."
                    }
                )

            existing_appointments = Pet.objects.filter(
                doctor=doctor,
                visit_date=visit_date
            )

            new_time = datetime.combine(visit_date, appointment_time)

            for appointment in existing_appointments:
                existing_time = datetime.combine(
                    visit_date,
                    appointment.appointment_time
                )

                difference = abs(new_time - existing_time)

                if difference < timedelta(minutes=30):
                    return render(
                        request,
                        "pets/add_pet.html",
                        {
                            "form": form,
                            "error": "This doctor already has another appointment within 30 minutes."
                        }
                    )

            pet = form.save()

            return render(
                request,
                "pets/appointment_confirmation.html",
                {
                    "pet": pet
                }
            )

    else:
        form = PetForm()

    return render(
        request,
        "pets/add_pet.html",
        {
            "form": form,
            "title": "Add New Pet"
        }
    )


def edit_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)

    if request.method == "POST":
        form = PetForm(request.POST, instance=pet)

        if form.is_valid():
            form.save()
            return redirect("pet_list")

    else:
        form = PetForm(instance=pet)

    return render(
        request,
        "pets/add_pet.html",
        {
            "form": form,
            "title": "Edit Pet"
        }
    )


def delete_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    pet.delete()
    return redirect("pet_list")


def statistics(request):
    total_pets = Pet.objects.count()

    species_stats = Pet.objects.values("species").annotate(
        total=Count("species")
    )

    return render(
        request,
        "pets/statistics.html",
        {
            "total_pets": total_pets,
            "species_stats": species_stats,
        },
    )


def available_times(request):
    doctor = request.GET.get("doctor")
    visit_date = request.GET.get("visit_date")

    all_times = [
        "09:00:00",
        "10:00:00",
        "11:00:00",
        "12:00:00",
        "01:00:00",
        "02:00:00",
        "03:00:00",
        "04:00:00",
    ]

    booked = []

    if doctor and visit_date:
        booked = list(
            Pet.objects.filter(
                doctor=doctor,
                visit_date=visit_date
            ).values_list("appointment_time", flat=True)
        )

        booked = [str(t) for t in booked]

    available = [t for t in all_times if t not in booked]

    return render(
        request,
        "pets/available_times.html",
        {
            "doctor": doctor,
            "visit_date": visit_date,
            "available": available,
        },
    )


def request_edit(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)

    if request.method == "POST":
        form = EditRequestForm(request.POST)

        if form.is_valid():
            edit_request = form.save(commit=False)
            edit_request.pet = pet
            edit_request.save()
            return redirect("pet_list")

    else:
        form = EditRequestForm()

    return render(
        request,
        "pets/request_edit.html",
        {
            "form": form,
            "pet": pet,
        },
    )