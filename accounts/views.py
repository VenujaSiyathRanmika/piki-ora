from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Patient


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, "accounts/register.html")

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )

        Patient.objects.create(user=user)

        messages.success(request, "Registration successful.")
        return redirect("login")

    return render(request, "accounts/register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("dashboard")

        messages.error(request, "Invalid username or password.")

    return render(request, "accounts/login.html")


def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("login")

    return render(request, "accounts/logout.html")


@api_view(["GET"])
def csrf_token(request):
    from django.middleware.csrf import get_token

    return Response({
        "csrfToken": get_token(request)
    })


@api_view(["POST"])
def api_login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    login_type = request.data.get("loginType", "patient")

    user = authenticate(
        request,
        username=username,
        password=password
    )

    if user is None:
        return Response(
            {"error": "Incorrect username or password."},
            status=400
        )

    if login_type == "admin" and not user.is_staff:
        return Response(
            {"error": "This account is not an administrator."},
            status=403
        )

    if login_type == "patient" and user.is_staff:
        return Response(
            {"error": "Please use Admin Login for this account."},
            status=403
        )

    login(request, user)

    return Response({
        "message": "Login successful.",
        "is_admin": user.is_staff,
        "username": user.username
    })


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def api_logout(request):
    logout(request)

    return Response({
        "message": "Logged out successfully."
    })

def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None and user.is_staff:
            login(request, user)
            return redirect("dashboard")

        messages.error(
            request,
            "Invalid administrator username or password."
        )

    return render(request, "accounts/admin_login.html")
