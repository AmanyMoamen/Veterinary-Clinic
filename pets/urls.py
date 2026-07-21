from django.urls import path
from . import views

urlpatterns = [
    path("", views.pet_list, name="pet_list"),
    path("add/", views.add_pet, name="add_pet"),
    path("edit/<int:pet_id>/", views.edit_pet, name="edit_pet"),
    path("delete/<int:pet_id>/", views.delete_pet, name="delete_pet"),

    path("statistics/", views.statistics, name="statistics"),

    # Available Times
    path("available-times/", views.available_times, name="available_times"),
]