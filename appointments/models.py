from django.db import models
from django.db.models import Q
from doctors.models import Doctor


class AppointmentSlot(models.Model):
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name="appointment_slots"
    )
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        ordering = ["date", "start_time"]
        constraints = [
            models.UniqueConstraint(
                fields=["doctor", "date", "start_time"],
                name="unique_doctor_slot"
            )
        ]

    def __str__(self):
        return (
            f"Dr. {self.doctor.first_name} {self.doctor.last_name} - "
            f"{self.date} {self.start_time}"
        )


class Appointment(models.Model):
    STATUS_CHOICES = [
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
    ]

    patient = models.ForeignKey(
        "accounts.Patient",
        on_delete=models.CASCADE,
        related_name="appointments"
    )

    slot = models.ForeignKey(
        AppointmentSlot,
        on_delete=models.CASCADE,
        related_name="appointments"
    )

    reason = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="confirmed"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-slot__date", "-slot__start_time"]
        constraints = [
            models.UniqueConstraint(
                fields=["slot"],
                condition=Q(status="confirmed"),
                name="unique_confirmed_appointment_per_slot"
            )
        ]

    def __str__(self):
        return (
            f"{self.patient.user.first_name} "
            f"{self.patient.user.last_name} - "
            f"{self.slot}"
        )