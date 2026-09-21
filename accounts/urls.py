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
]