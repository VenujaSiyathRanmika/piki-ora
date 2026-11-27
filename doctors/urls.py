from django.urls import path
from . import views

urlpatterns = [
    path("api/", views.doctor_list, name="doctor-list"),
    path("api/add/", views.add_doctor, name="add-doctor"),
    path(
        "api/<int:doctor_id>/edit/",
        views.edit_doctor,
        name="edit-doctor"
    ),
    path(
        "api/<int:doctor_id>/delete/",
        views.delete_doctor,
        name="delete-doctor"
    ),
]
