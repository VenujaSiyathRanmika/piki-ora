
import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Reset a specific patient account password."

    def handle(self, *args, **options):
        username = os.environ.get("RESET_PATIENT_USERNAME", "").strip()
        password = os.environ.get("RESET_PATIENT_PASSWORD", "")

        if not username or not password:
            raise CommandError("Patient reset environment variables are missing.")

        User = get_user_model()

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise CommandError("Patient username was not found.")

        if user.is_staff or user.is_superuser:
            raise CommandError("Refusing to modify an administrator account.")

        if not hasattr(user, "patient_profile"):
            raise CommandError("This account has no patient profile.")

        user.set_password(password)
        user.save(update_fields=["password"])

        self.stdout.write(
            self.style.SUCCESS("Patient password reset successfully.")
        )
