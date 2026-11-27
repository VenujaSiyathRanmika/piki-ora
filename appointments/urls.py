from django.urls import path, include
from . import views


urlpatterns = [
    path(
        "book/",
        views.book_appointment,
        name="book_appointment",
    ),
    path(
        "my/",
        views.my_appointments,
        name="my_appointments",
    ),
    path(
        "edit/<int:appointment_id>/",
        views.edit_appointment,
        name="edit_appointment",
    ),
    path(
        "cancel/<int:appointment_id>/",
        views.cancel_appointment,
        name="cancel_appointment",
    ),
    path(
        "api/slots/",
        views.appointment_slot_list,
        name="appointment-slot-list",
    ),
    path(
        "api/<int:appointment_id>/cancel/",
        views.cancel_appointment_api,
        name="cancel-appointment-api",
    ),
    path(
        "api/",
        include("appointments.api_urls"),
    ),
]
