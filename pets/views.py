from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import connection
from django.db.models import Count
from datetime import datetime, timedelta, date
from django.http import FileResponse, JsonResponse

from reportlab.pdfgen import canvas     
from io import BytesIO

from .models import Pet, EditRequest, Doctor, DoctorSchedule
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
        
        print("LOGIN DEBUG - DB:", connection.vendor)
        print("LOGIN DEBUG - USER EXISTS:", User.objects.filter(username=username).exists())

        user = authenticate(
            request,
            username=username,
            password=password
        )   

        print("LOGIN DEBUG - PETS COUNT:", Pet.objects.count())
        print("LOGIN DEBUG - APPOINTMENTS COUNT:", Pet.objects.filter(appointment_time__isnull=False).count())

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

        selected_doctor = get_object_or_404(
            Doctor,
            id=doctor
        )

        pets = pets.filter(
            doctor=selected_doctor.name
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

        form = PetForm(
            request.POST,
            user=request.user
        )

        if form.is_valid():

            doctor = form.cleaned_data["doctor"]

            visit_date = form.cleaned_data["visit_date"]

            # =========================
            # Get Doctor Branch
            # =========================

            branch = doctor.branch

            # =========================
            # Make Sure Doctor Has Branch
            # =========================

            if not branch:

                return render(
                    request,
                    "pets/add_pet.html",
                    {
                        "form": form,
                        "error": (
                            "This doctor is not assigned "
                            "to any branch."
                        )
                    }
                )

            # =========================
            # Appointment Time
            # =========================

            appointment_time = form.cleaned_data[
                "appointment_time"
            ]

            # Convert string to datetime.time
            if isinstance(appointment_time, str):

                appointment_time_obj = datetime.strptime(
                    appointment_time,
                    "%H:%M"
                ).time()

            else:

                appointment_time_obj = appointment_time
  
            # =========================
            # Check Doctor Schedule
            # =========================

            schedules = DoctorSchedule.objects.filter(
                doctor=doctor,
                branch=branch,
                date=visit_date
            )

            if not schedules.exists():

                return render(
                    request,
                    "pets/add_pet.html",
                    {
                        "form": form,
                        "error": (
                            "This doctor has no schedule "
                            "for the selected date."
                        )
                    }
                )

            # Check if appointment is inside one of
            # the doctor's shifts

            appointment_end_time = (
                datetime.combine(
                    visit_date,
                    appointment_time_obj
                )
                + timedelta(
                    minutes=doctor.consultation_time
                )
            ).time()

            valid_schedule = False

            for schedule in schedules:

                if (
                    schedule.start_time
                    <= appointment_time_obj
                    and
                    appointment_end_time
                    <= schedule.end_time
                ):

                    valid_schedule = True
                    break

            if not valid_schedule:

                return render(
                    request,
                    "pets/add_pet.html",
                    {
                        "form": form,
                        "error": (
                            "The selected appointment time "
                            "is outside the doctor's working hours."
                        )
                    }
                )

            # =========================
            # Maximum Appointments
            # =========================

            appointments_count = Pet.objects.filter(
                doctor=doctor.name,
                branch=branch,
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
                doctor=doctor.name,
                branch=branch,
                visit_date=visit_date
            )

            # New appointment datetime
            new_time = datetime.combine(
                visit_date,
                appointment_time_obj
            )

            # =========================
            # Check Consultation Time
            # =========================

            for appointment in existing_appointments:

                existing_appointment_time = (
                    appointment.appointment_time
                )

                # If stored as string, convert it
                # to datetime.time
                if isinstance(
                    existing_appointment_time,
                    str
                ):

                    existing_appointment_time = datetime.strptime(
                        existing_appointment_time,
                        "%H:%M"
                    ).time()

                existing_time = datetime.combine(
                    visit_date,
                    existing_appointment_time
                )

                difference = abs(
                    new_time - existing_time
                )

                # Prevent booking during doctor's
                # consultation time
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

            # Save doctor name
            pet.doctor = doctor.name

            # Assign appointment to doctor's branch
            pet.branch = branch

            # Save the user who created the appointment
            pet.created_by = request.user

            pet.save()     

            return redirect(
                "appointment_confirmation",
                pet_id=pet.id
            )

    else:

        form = PetForm(
            user=request.user
        )

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

    doctor_id = request.GET.get("doctor")
    visit_date = request.GET.get("visit_date")

    booked = []
    available = []
    all_times = []

    consultation_time = 0

    if doctor_id and visit_date:

        doctor_obj = get_object_or_404(
            Doctor,
            id=doctor_id
        )

        # Check Receptionist Branch
        if (
            not request.user.is_superuser
            and request.user.profile.role == "Receptionist"
        ):

            receptionist_branch = request.user.profile.branch

            if (
                not receptionist_branch
                or doctor_obj.branch != receptionist_branch
            ):

                return JsonResponse(
                    {
                        "error": (
                            "You are not allowed to view "
                            "appointments for this branch."
                        )
                    },
                    status=403
                )

        consultation_time = doctor_obj.consultation_time

        selected_date = datetime.strptime(
            visit_date,
            "%Y-%m-%d"
        ).date()
        
        # =========================
        # Get Doctor Schedule
        # =========================

        schedules = DoctorSchedule.objects.filter(
            doctor=doctor_obj,
            date=selected_date
        ).order_by(
            "start_time"
        )

        # =========================
        # Get Existing Appointments
        # =========================

        existing_appointments = Pet.objects.filter(
            doctor=doctor_obj.name,
            visit_date=selected_date
        ).exclude(
            status__iexact="Cancelled"
        )

        # =========================
        # Get Booked Times
        # =========================

        for appointment in existing_appointments:

            appointment_time = appointment.appointment_time

            if isinstance(
                appointment_time,
                str
            ):

                appointment_time = datetime.strptime(
                    appointment_time,
                    "%H:%M"
                ).time()

            time_string = appointment_time.strftime(
                "%H:%M"
            )

            if time_string not in booked:

                booked.append(
                    time_string
                )

        # =========================
        # Generate Appointment Times
        # =========================

        for schedule in schedules:

            current_datetime = datetime.combine(
                selected_date,
                schedule.start_time
            )

            end_datetime = datetime.combine(
                selected_date,
                schedule.end_time
            )

            while (
                current_datetime
                + timedelta(
                    minutes=consultation_time
                )
                <= end_datetime
            ):

                current_time = current_datetime.time()

                time_string = current_time.strftime(
                    "%H:%M"
                )

                if time_string not in all_times:

                    all_times.append(
                        time_string
                    )

                current_datetime += timedelta(
                    minutes=consultation_time
                )

        # =========================
        # Sort Times
        # =========================

        all_times.sort()
        booked.sort()

        # =========================
        # Check Available Times
        # =========================

        for time_string in all_times:

            current_time = datetime.strptime(
                time_string,
                "%H:%M"
            ).time()

            current_datetime = datetime.combine(
                selected_date,
                current_time
            )

            new_start = current_datetime

            new_end = (
                current_datetime
                + timedelta(
                    minutes=consultation_time
                )
            )

            is_available = True

            # =========================
            # Compare With Existing
            # Appointments
            # =========================

            for appointment in existing_appointments:

                existing_time = appointment.appointment_time

                if isinstance(
                    existing_time,
                    str
                ):

                    existing_time = datetime.strptime(
                        existing_time,
                        "%H:%M"
                    ).time()

                existing_datetime = datetime.combine(
                    selected_date,
                    existing_time
                )

                existing_start = existing_datetime

                existing_end = (
                    existing_datetime
                    + timedelta(
                        minutes=consultation_time
                    )
                )

                # =========================
                # Check Overlap
                # =========================

                if (
                    new_start < existing_end
                    and
                    new_end > existing_start
                ):

                    is_available = False

                    break

            if is_available:

                available.append(
                    time_string
                )

    # =========================
    # Return JSON
    # =========================

    return JsonResponse(
        {
            "times": all_times,
            "booked": booked,
            "available": available,
            "consultation_time": consultation_time,
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
            doctor=doctor.name
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