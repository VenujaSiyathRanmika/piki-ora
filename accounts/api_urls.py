from django.urls import path
from . import api_views

urlpatterns = [
    path("csrf/", api_views.csrf_token, name="api_csrf"),
    path("login/", api_views.patient_login, name="api_patient_login"),
    path("admin-login/", api_views.admin_login, name="api_admin_login"),
    path("logout/", api_views.patient_logout, name="api_patient_logout"),
]
