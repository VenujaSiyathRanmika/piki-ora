from django.db import models


class Doctor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    specialisation = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name}"