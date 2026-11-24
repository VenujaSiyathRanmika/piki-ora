
from django.urls import path
from . import views

urlpatterns = [
    path("api/", views.doctor_list_api, name="doctor_list_api"),
]
