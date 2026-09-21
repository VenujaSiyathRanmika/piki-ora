from django import forms

from appointments.models import Appointment, AppointmentSlot
from doctors.models import Doctor


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor

        fields = [
            "first_name",
            "last_name",
            "specialisation",
            "email",
            "phone",
            "bio",
        ]

        widgets = {
            "first_name": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "specialisation": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control"}
            ),
            "phone": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "bio": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                }
            ),
        }


class AppointmentSlotForm(forms.ModelForm):
    class Meta:
        model = AppointmentSlot

        fields = [
            "doctor",
            "date",
            "start_time",
            "end_time",
        ]

        widgets = {
            "doctor": forms.Select(
                attrs={"class": "form-control"}
            ),
            "date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
            "start_time": forms.TimeInput(
                attrs={
                    "class": "form-control",
                    "type": "time",
                }
            ),
            "end_time": forms.TimeInput(
                attrs={
                    "class": "form-control",
                    "type": "time",
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()

        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")

        if start_time and end_time and end_time <= start_time:
            raise forms.ValidationError(
                "End time must be later than start time."
            )

        return cleaned_data


class AdminAppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment

        fields = [
            "slot",
            "reason",
            "status",
        ]

        widgets = {
            "slot": forms.Select(
                attrs={"class": "form-control"}
            ),
            "reason": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                }
            ),
            "status": forms.Select(
                attrs={"class": "form-control"}
            ),
        }