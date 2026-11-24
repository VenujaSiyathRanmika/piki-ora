
# Trusted origins for Django CSRF protection
CSRF_TRUSTED_ORIGINS = [
    "https://piki-ora-frontend-rmbx.onrender.com",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

# Allowed origins for frontend requests
CORS_ALLOWED_ORIGINS = [
    "https://piki-ora-frontend-rmbx.onrender.com",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

# Allow session cookies to be sent with cross-origin requests
CORS_ALLOW_CREDENTIALS = True

# Django REST Framework configuration
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
}
