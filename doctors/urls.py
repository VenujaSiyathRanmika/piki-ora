from django.urls import path
from . import views

urlpatterns = [
    path("", views.doctor_list_api, name="doctor_list_api"),
]
