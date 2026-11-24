from django.urls import path
from . import admin_api

urlpatterns = [
    path("appointments/", admin_api.admin_appointments, name="admin_api_appointments"),
    path("doctors/", admin_api.admin_doctors, name="admin_api_doctors"),
    path("slots/", admin_api.admin_slots, name="admin_api_slots"),
]
