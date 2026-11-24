
import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Safely reset an existing administrator password."

    def handle(self, *args, **options):
        username = os.environ.get("RESET_ADMIN_USERNAME")
        password = os.environ.get("RESET_ADMIN_PASSWORD")

        if not username or not password:
            raise CommandError(
                "Set RESET_ADMIN_USERNAME and RESET_ADMIN_PASSWORD first."
            )

        if len(password) < 12:
            raise CommandError("Use a password of at least 12 characters.")

        User = get_user_model()

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise CommandError("Admin account not found. No changes made.")

        if not user.is_staff:
            raise CommandError("Account is not a staff account. No changes made.")

        user.set_password(password)
        user.save(update_fields=["password"])

        self.stdout.write(self.style.SUCCESS(
            "Admin password reset successfully."
        ))

