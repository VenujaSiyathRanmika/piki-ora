from django.db import models
from django.contrib.auth.models import User


class Patient(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="patient_profile"
    )
    phone = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    address = models.TextField()

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"