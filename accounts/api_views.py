import json

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.views.decorators.http import require_http_methods


@ensure_csrf_cookie
def csrf_token(request):
    return JsonResponse({
        "message": "CSRF cookie ready",
        "csrfToken": get_token(request),
    })


@require_http_methods(["GET", "POST"])
@csrf_protect
def patient_login(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return JsonResponse({
                "authenticated": True,
                "username": request.user.username,
                "is_staff": request.user.is_staff,
            })

        return JsonResponse({"authenticated": False})

    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse(
            {"error": "Invalid request data."},
            status=400,
        )

    username = data.get("username", "").strip()
    password = data.get("password", "")

    user = authenticate(
        request,
        username=username,
        password=password,
    )

    if user is None:
        return JsonResponse(
            {"error": "Invalid username or password."},
            status=400,
        )

    if user.is_staff:
        return JsonResponse(
            {"error": "Please use the administrator login."},
            status=403,
        )

    if not hasattr(user, "patient_profile"):
        return JsonResponse(
            {"error": "A patient profile is required."},
            status=403,
        )

    login(request, user)

    return JsonResponse({
        "message": "Login successful.",
        "username": user.username,
    })


@require_http_methods(["POST"])
@csrf_protect
def patient_logout(request):
    logout(request)

    return JsonResponse({
        "message": "Logged out successfully.",
    })


@require_http_methods(["GET", "POST"])
@csrf_protect
def admin_login(request):
    if request.method == "GET":
        if request.user.is_authenticated and request.user.is_staff:
            return JsonResponse({
                "authenticated": True,
                "username": request.user.username,
                "is_staff": True,
            })

        return JsonResponse({"authenticated": False})

    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse(
            {"error": "Invalid request data."},
            status=400,
        )

    username = data.get("username", "").strip()
    password = data.get("password", "")

    user = authenticate(
        request,
        username=username,
        password=password,
    )

    if (
        user is None
        or not user.is_active
        or not user.is_staff
    ):
        return JsonResponse(
            {"error": "Invalid administrator username or password."},
            status=403,
        )

    login(request, user)

    return JsonResponse({
        "message": "Administrator login successful.",
        "username": user.username,
        "is_staff": True,
    })