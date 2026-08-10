from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.db.models import Count
from datetime import datetime, timedelta, date
from django.http import FileResponse, JsonResponse

from reportlab.pdfgen import canvas
from io import BytesIO

from .models import Pet, EditRequest, Doctor
from .forms import PetForm, EditRequestForm
from .decorators import role_required


# =========================
# Login
# =========================

def login_view(request):

    if request.user.is_authenticated:
        return redirect("role_dashboard")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect("role_dashboard")

        return render(
            request,
            "pets/login.html",
            {
                "error": "Invalid username or password."
            }
        )

    return render(
        request,
        "pets/login.html"
    )


# =========================
# Logout
# =========================

def logout_view(request):

    logout(request)

    return redirect("login")


# =========================
# Role Dashboard
# =========================

def role_dashboard(request):

    if not request.user.is_authenticated:
        return redirect("login")

    if request.user.is_superuser:
        return redirect("statistics")

    try:
        role = request.user.profile.role

    except AttributeError:
        return redirect("unauthorized")

    if role == "Admin":
        return redirect("statistics")

    elif role == "Receptionist":
        return redirect("pet_list")

    elif role == "Doctor":
        return redirect("doctor_dashboard")

    return redirect("unauthorized")


# =========================
# Unauthorized
# =========================

def unauthorized(request):

    return render(
        request,
        "pets/unauthorized.html"
    )


# =========================
# Pet List
# =========================

@role_required("Receptionist")
def pet_list(request):

    pets = Pet.objects.all().order_by(
        "visit_date",
        "appointment_time"
    )

    # Get all doctors
    doctors = Doctor.objects.all()

    filter_type = request.GET.get("filter")
    doctor = request.GET.get("doctor")

    # =========================
    # Filters
    # =========================

    if filter_type == "today":

        pets = pets.filter(
            visit_date=date.today()
        )

    elif filter_type == "week":

        today = date.today()

        end_week = today + timedelta(days=7)

        pets = pets.filter(
            visit_date__gte=today,
            visit_date__lte=end_week
        )

    elif filter_type == "normal":

        pets = pets.filter(
            priority="Normal"
        )

    elif filter_type == "urgent":

        pets = pets.filter(
            priority="Urgent"
        )

    elif filter_type == "emergency":

        pets = pets.filter(
            priority="Emergency"
        )

    # =========================
    # Filter By Doctor
    # =========================

    if doctor:

        pets = pets.filter(
            doctor_id=doctor
        )

    return render(
        request,
        "pets/index.html",
        {
            "pets": pets,
            "doctors": doctors,
        },
    )


# =========================
# Add Pet
# =========================

@role_required("Admin", "Receptionist")
def add_pet(request):

    if request.method == "POST":

        form = PetForm(request.POST)

        if form.is_valid():

            doctor = form.cleaned_data["doctor"]

            visit_date = form.cleaned_data["visit_date"]

            appointment_time = datetime.strptime(
                form.cleaned_data["appointment_time"],
                "%H:%M"
            ).time()

            # =========================
            # Maximum Appointments
            # =========================

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
                        "error": (
                            "This doctor already has the maximum "
                            "number of appointments for this day."
                        )
                    }
                )

            # =========================
            # Check Appointment Time
            # =========================

            existing_appointments = Pet.objects.filter(
                doctor=doctor,
                visit_date=visit_date
            )

            new_time = datetime.combine(
                visit_date,
                appointment_time
            )

            for appointment in existing_appointments:

                existing_time = datetime.combine(
                    visit_date,
                    appointment.appointment_time
                )

                difference = abs(
                    new_time - existing_time
                )

                if difference < timedelta(
                    minutes=doctor.consultation_time
                ):

                    return render(
                        request,
                        "pets/add_pet.html",
                        {
                            "form": form,
                            "error": (
                                f"This doctor already has another "
                                f"appointment within "
                                f"{doctor.consultation_time} minutes."
                            )
                        }
                    )

            # =========================
            # Save Pet
            # =========================

            pet = form.save(commit=False)

            pet.status = "Waiting"

            pet.save()

            return redirect(
                "appointment_confirmation",
                pet_id=pet.id
            )

    else:

        form = PetForm()

    pets_today = Pet.objects.none()

    return render(
        request,
        "pets/add_pet.html",
        {
            "form": form,
            "title": "Add New Pet",
            "pets_today": pets_today,
        }
    )


# =========================
# Appointment Confirmation
# =========================

@role_required("Admin", "Receptionist")
def appointment_confirmation(request, pet_id):

    pet = get_object_or_404(
        Pet,
        id=pet_id
    )

    return render(
        request,
        "pets/appointment_confirmation.html",
        {
            "pet": pet
        }
    )


# =========================
# Edit Pet
# =========================

@role_required("Admin", "Receptionist")
def edit_pet(request, pet_id):

    pet = get_object_or_404(
        Pet,
        id=pet_id
    )

    if request.method == "POST":

        form = PetForm(
            request.POST,
            instance=pet
        )

        if form.is_valid():

            form.save()

            return redirect("pet_list")

    else:

        form = PetForm(
            instance=pet
        )

    return render(
        request,
        "pets/add_pet.html",
        {
            "form": form,
            "title": "Edit Pet"
        }
    )


# =========================
# Delete Pet
# =========================

@role_required("Admin", "Receptionist")
def delete_pet(request, pet_id):

    pet = get_object_or_404(
        Pet,
        id=pet_id
    )

    pet.delete()

    return redirect("pet_list")


# =========================
# Statistics
# =========================

@role_required("Admin")
def statistics(request):

    total_pets = Pet.objects.count()

    species_stats = Pet.objects.values(
        "species"
    ).annotate(
        total=Count("species")
    )

    waiting = Pet.objects.filter(
        status="Waiting"
    ).count()

    arrived = Pet.objects.filter(
        status="Arrived"
    ).count()

    cancelled = Pet.objects.filter(
        status="Cancelled"
    ).count()

    return render(
        request,
        "pets/statistics.html",
        {
            "total_pets": total_pets,
            "species_stats": species_stats,
            "waiting": waiting,
            "arrived": arrived,
            "cancelled": cancelled,
        },
    )


# =========================
# Available Times
# =========================

@role_required("Admin", "Receptionist")
def available_times(request):

    doctor = request.GET.get("doctor")
    visit_date = request.GET.get("visit_date")

    doctor_obj = None
    booked = []
    available = []

    # All clinic appointment times
    all_times = [
        "09:00",
        "09:30",
        "10:00",
        "10:30",
        "11:00",
        "11:30",
        "12:00",
        "12:30",
        "13:00",
    ]

    if doctor and visit_date:

        doctor_obj = get_object_or_404(
            Doctor,
            id=doctor
        )

        booked = list(
            Pet.objects.filter(
                doctor=doctor_obj,
                visit_date=visit_date
            ).values_list(
                "appointment_time",
                flat=True
            )
        )

        booked = [
            t.strftime("%H:%M")
            for t in booked
        ]

        # Remove booked times
        available = [
            time for time in all_times
            if time not in booked
        ]

    return render(
        request,
        "pets/available_times.html",
        {
            "doctor": doctor_obj,
            "visit_date": visit_date,
            "booked": booked,
            "available": available,
        }
    )

# =========================
# Request Edit
# =========================

@role_required("Admin", "Receptionist")
def request_edit(request, pet_id):

    pet = get_object_or_404(
        Pet,
        id=pet_id
    )

    if request.method == "POST":

        form = EditRequestForm(
            request.POST
        )

        if form.is_valid():

            edit_request = form.save(
                commit=False
            )

            edit_request.pet = pet

            edit_request.user = request.user

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


# =========================
# Appointment PDF
# =========================

@role_required("Admin", "Receptionist")
def download_pdf(request, pet_id):

    pet = get_object_or_404(
        Pet,
        id=pet_id
    )

    buffer = BytesIO()

    pdf = canvas.Canvas(buffer)

    pdf.setTitle(
        "Appointment Slip"
    )

    pdf.setFont(
        "Helvetica-Bold",
        18
    )

    pdf.drawString(
        180,
        800,
        "PetCare Veterinary Clinic"
    )

    pdf.setFont(
        "Helvetica",
        14
    )

    pdf.drawString(
        220,
        775,
        "Appointment Slip"
    )

    pdf.line(
        50,
        760,
        550,
        760
    )

    y = 730

    pdf.setFont(
        "Helvetica",
        12
    )

    pdf.drawString(
        60,
        y,
        f"Appointment Number: {pet.appointment_number}"
    )

    y -= 25

    pdf.drawString(
        60,
        y,
        f"Pet Name: {pet.name}"
    )

    y -= 25

    pdf.drawString(
        60,
        y,
        f"Owner Name: {pet.owner_name}"
    )

    y -= 25

    pdf.drawString(
        60,
        y,
        f"Doctor: {pet.doctor}"
    )

    y -= 25

    pdf.drawString(
        60,
        y,
        f"Visit Date: {pet.visit_date}"
    )

    y -= 25

    pdf.drawString(
        60,
        y,
        f"Appointment Time: {pet.appointment_time}"
    )

    y -= 25

    pdf.drawString(
        60,
        y,
        f"Priority: {pet.priority}"
    )

    y -= 25

    pdf.drawString(
        60,
        y,
        f"Visit Reason: {pet.visit_reason}"
    )

    pdf.save()

    buffer.seek(0)

    return FileResponse(
        buffer,
        as_attachment=True,
        filename=f"{pet.appointment_number}.pdf"
    )


# =========================
# Doctor Dashboard
# =========================

@role_required("Doctor")
def doctor_dashboard(request):

    today = date.today()

    appointments = Pet.objects.all()

    filter_type = request.GET.get(
        "filter",
        "all"
    )

    if filter_type == "today":

        appointments = appointments.filter(
            visit_date=today
        )

    elif filter_type == "week":

        appointments = appointments.filter(
            visit_date__gte=today,
            visit_date__lte=today + timedelta(days=7)
        )

    elif filter_type == "all":

        pass

    appointments = appointments.order_by(
        "doctor",
        "appointment_time"
    )

    doctors = Doctor.objects.all()

    dashboard = []

    for doctor in doctors:

        doctor_appointments = appointments.filter(
            doctor=doctor
        )

        dashboard.append(
            {
                "doctor": doctor.name,
                "appointments": doctor_appointments,
                "count": doctor_appointments.count(),
            }
        )

    return render(
        request,
        "pets/doctor_dashboard.html",
        {
            "dashboard": dashboard,
            "today": today,
            "filter": filter_type,
        },
    )


# =========================
# Mark Arrived
# =========================

@role_required("Admin", "Receptionist")
def mark_arrived(request, pet_id):

    pet = get_object_or_404(
        Pet,
        id=pet_id
    )

    pet.status = "Arrived"

    pet.save()

    return redirect(
        "pet_list"
    )


# =========================
# Mark Cancelled
# =========================

@role_required("Admin", "Receptionist")
def mark_cancelled(request, pet_id):

    pet = get_object_or_404(
        Pet,
        id=pet_id
    )

    pet.status = "Cancelled"

    pet.save()

    return redirect(
        "pet_list"
    )