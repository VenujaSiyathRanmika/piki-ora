from django.urls import path

from . import admin_views
from . import views


urlpatterns = [
    # Patient dashboard
    path(
        "",
        views.patient_dashboard,
        name="patient_dashboard",
    ),

    # Custom administrator dashboard
    path(
        "admin/",
        admin_views.admin_dashboard,
        name="admin_dashboard",
    ),

    # Doctors
    path(
        "admin/doctors/",
        admin_views.doctor_list,
        name="admin_doctors",
    ),

    path(
        "admin/doctors/add/",
        admin_views.doctor_create,
        name="admin_doctor_add",
    ),

    path(
        "admin/doctors/<int:doctor_id>/edit/",
        admin_views.doctor_edit,
        name="admin_doctor_edit",
    ),

    path(
        "admin/doctors/<int:doctor_id>/delete/",
        admin_views.doctor_delete,
        name="admin_doctor_delete",
    ),

    # Appointment slots
    path(
        "admin/slots/",
        admin_views.slot_list,
        name="admin_slots",
    ),

    path(
        "admin/slots/add/",
        admin_views.slot_create,
        name="admin_slot_add",
    ),

    path(
        "admin/slots/<int:slot_id>/edit/",
        admin_views.slot_edit,
        name="admin_slot_edit",
    ),

    path(
        "admin/slots/<int:slot_id>/delete/",
        admin_views.slot_delete,
        name="admin_slot_delete",
    ),

    # Appointments
    path(
        "admin/appointments/",
        admin_views.appointment_list,
        name="admin_appointments",
    ),

    path(
        "admin/appointments/<int:appointment_id>/edit/",
        admin_views.appointment_edit,
        name="admin_appointment_edit",
    ),

    # Patients
    path(
        "admin/patients/",
        admin_views.patient_list,
        name="admin_patients",
    ),

    path(
        "admin/patients/<int:patient_id>/toggle/",
        admin_views.patient_toggle_status,
        name="admin_patient_toggle",
    ),
]