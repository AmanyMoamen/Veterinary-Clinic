from django.urls import path
from . import views

urlpatterns = [

    # =========================
    # Authentication
    # =========================

    path(
        "login/",
        views.login_view,
        name="login"
    ),

    path(
        "logout/",
        views.logout_view,
        name="logout"
    ),

    path(
        "dashboard/",
        views.role_dashboard,
        name="role_dashboard"
    ),

    path(
        "unauthorized/",
        views.unauthorized,
        name="unauthorized"
    ),


    # =========================
    # Pets
    # =========================

    path(
        "",
        views.pet_list,
        name="pet_list"
    ),

    path(
        "add/",
        views.add_pet,
        name="add_pet"
    ),

    path(
        "appointment-confirmation/<int:pet_id>/",
        views.appointment_confirmation,
        name="appointment_confirmation"
    ),          

    path(
        "edit/<int:pet_id>/",
        views.edit_pet,
        name="edit_pet"
    ),

    path(
        "delete/<int:pet_id>/",
        views.delete_pet,
        name="delete_pet"
    ),


    # =========================
    # Statistics
    # =========================

    path(
        "statistics/",
        views.statistics,
        name="statistics"
    ),


    # =========================
    # Available Times
    # =========================

    path(
        "available-times/",
        views.available_times,
        name="available_times"
    ),


    # =========================
    # Request Edit
    # =========================

    path(
        "request-edit/<int:pet_id>/",
        views.request_edit,
        name="request_edit"
    ),


    # =========================
    # Appointment PDF
    # =========================

    path(
        "appointment-pdf/<int:pet_id>/",
        views.download_pdf,
        name="appointment_pdf"
    ),


    # =========================
    # Doctor Dashboard
    # =========================

    path(
        "doctor-dashboard/",
        views.doctor_dashboard,
        name="doctor_dashboard"
    ),


    # =========================
    # Appointment Status
    # =========================

    path(
        "arrived/<int:pet_id>/",
        views.mark_arrived,
        name="mark_arrived"
    ),

    path(
        "cancel/<int:pet_id>/",
        views.mark_cancelled,
        name="mark_cancelled"
    ),
]