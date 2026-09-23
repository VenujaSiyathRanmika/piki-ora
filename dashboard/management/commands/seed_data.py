from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.management.base import BaseCommand

from doctors.models import Doctor
from appointments.models import AppointmentSlot


class Command(BaseCommand):
    help = "Create initial Piki Ora production data."

    def handle(self, *args, **options):

        User = get_user_model()

        # Create administrator account if it does not already exist.
        admin_username = "admin"
        admin_email = "admin@piki-ora.co.nz"
        admin_password = "admin"

        if not User.objects.filter(username=admin_username).exists():
            User.objects.create_superuser(
                username=admin_username,
                email=admin_email,
                password=admin_password,
            )

            self.stdout.write(
                self.style.SUCCESS(
                    "Administrator account created."
                )
            )
        else:
            self.stdout.write(
                "Administrator account already exists."
            )

        # Create doctors.
        doctors = [
            {
                "first_name": "Sarah",
                "last_name": "Williams",
                "specialisation": "General Practitioner",
                "email": "sarah.williams@piki-ora.co.nz",
                "phone": "0211111111",
                "bio": "General practitioner providing primary healthcare services.",
            },
            {
                "first_name": "James",
                "last_name": "Brown",
                "specialisation": "Family Medicine",
                "email": "james.brown@piki-ora.co.nz",
                "phone": "0212222222",
                "bio": "Family medicine specialist providing comprehensive healthcare.",
            },
            {
                "first_name": "Emily",
                "last_name": "Taylor",
                "specialisation": "Women's Health",
                "email": "emily.taylor@piki-ora.co.nz",
                "phone": "0213333333",
                "bio": "Women's health specialist providing patient-centred care.",
            },
        ]

        doctor_objects = []

        for doctor_data in doctors:
            doctor, created = Doctor.objects.get_or_create(
                email=doctor_data["email"],
                defaults=doctor_data,
            )

            doctor_objects.append(doctor)

            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created doctor: {doctor}"
                    )
                )
            else:
                self.stdout.write(
                    f"Doctor already exists: {doctor}"
                )

        # Create future appointment slots.
        tomorrow = timezone.localdate() + timedelta(days=1)

        slots = [
            (doctor_objects[0], tomorrow, "09:00", "09:30"),
            (doctor_objects[0], tomorrow, "10:00", "10:30"),
            (doctor_objects[1], tomorrow, "11:00", "11:30"),
            (doctor_objects[1], tomorrow, "14:00", "14:30"),
            (doctor_objects[2], tomorrow, "15:00", "15:30"),
        ]

        for doctor, date, start_time, end_time in slots:
            slot, created = AppointmentSlot.objects.get_or_create(
                doctor=doctor,
                date=date,
                start_time=start_time,
                defaults={
                    "end_time": end_time,
                },
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created slot: {slot}"
                    )
                )
            else:
                self.stdout.write(
                    f"Slot already exists: {slot}"
                )

        self.stdout.write(
            self.style.SUCCESS(
                "Piki Ora production data setup completed."
            )
        )