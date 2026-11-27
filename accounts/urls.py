
from django.urls import path

from . import views


urlpatterns = [
    path(
        "register/",
        views.register,
        name="register",
    ),

    path(
        "login/",
        views.login_view,
        name="login",
    ),

    path(
        "admin-login/",
        views.admin_login,
        name="admin_login",
    ),

    path(
        "logout/",
        views.logout_view,
        name="logout",
    ),

    # CSRF token for the React frontend
    path(
        "api/csrf/",
        views.csrf_token,
        name="csrf-token",
    ),
    path("api/login/", 
         views.api_login, 
         name="api-login"
    ),

    path("api/logout/",
        views.api_logout, 
        name="api_logout"),
]
