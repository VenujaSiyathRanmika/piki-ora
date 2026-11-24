
from django.urls import path
from . import api_views

urlpatterns = [
    path(
        "slots/",
        api_views.available_slots,
        name="api_available_slots",
    ),
    path(
        "my/",
        api_views.patient_appointments,
        name="api_patient_appointments",
    ),
    path(
        "cancel/<int:appointment_id>/",
        api_views.cancel_appointment_api,
        name="api_cancel_appointment",
    ),
]
