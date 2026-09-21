from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import PatientRegistrationForm


def register(request):
    if request.user.is_authenticated:
        return redirect("patient_dashboard")

    if request.method == "POST":
        form = PatientRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            messages.success(
                request,
                "Your patient account has been created successfully."
            )

            return redirect("patient_dashboard")
    else:
        form = PatientRegistrationForm()

    return render(
        request,
        "accounts/register.html",
        {
            "form": form,
        }
    )


def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect("admin_dashboard")

        return redirect("patient_dashboard")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is not None:
            login(request, user)

            if user.is_staff:
                return redirect("admin_dashboard")

            return redirect("patient_dashboard")

        messages.error(
            request,
            "Invalid username or password."
        )

    return render(
        request,
        "accounts/login.html"
    )


def admin_login(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect("admin_dashboard")

        logout(request)

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is not None and user.is_staff:
            login(request, user)

            return redirect("admin_dashboard")

        messages.error(
            request,
            "Invalid administrator credentials."
        )

    return render(
        request,
        "accounts/admin_login.html"
    )


@login_required
def logout_view(request):
    logout(request)

    return redirect("login")
