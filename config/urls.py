from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path


def home_view(request):
    if request.user.is_authenticated:
        return redirect("patient_dashboard")

    return redirect("login")


urlpatterns = [

    path(
        "",
        home_view,
        name="home",
    ),

    path(
        "admin/",
        admin.site.urls,
    ),

    path(
        "accounts/",
        include("accounts.urls"),
    ),

    path(
        "appointments/",
        include("appointments.urls"),
    ),

    path(
        "dashboard/",
        include("dashboard.urls"),
    ),
]