
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path


def home_view(request):
    if request.user.is_authenticated:
        return redirect("patient_dashboard")
    return redirect("login")


urlpatterns = [
    path("", home_view, name="home"),
    path("admin/", admin.site.urls),

    # Existing Assignment 1 website routes
    path("accounts/", include("accounts.urls")),
    path("appointments/", include("appointments.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("doctors/", include("doctors.urls")),

    # Assignment 2 API routes
    path("api/doctors/", include("doctors.urls")),
    path("api/appointments/", include("appointments.api_urls")),
    path("api/accounts/", include("accounts.api_urls")),
    path("api/admin/", include("appointments.admin_api_urls")),
]
