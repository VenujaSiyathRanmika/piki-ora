from django.urls import path

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
]