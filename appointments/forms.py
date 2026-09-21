from django import forms
from django.utils import timezone

from .models import Appointment, AppointmentSlot


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["slot", "reason"]

        widgets = {
            "slot": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
            "reason": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Please describe the reason for your appointment.",
                    "rows": 4,
                }
            ),
        }

    def __init__(self, *args, appointment=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.appointment = appointment

        today = timezone.localdate()

        available_slots = AppointmentSlot.objects.filter(
            date__gte=today
        ).exclude(
            appointments__status="confirmed"
        ).select_related(
            "doctor"
        ).order_by(
            "date",
            "start_time"
        )

        # When editing an existing appointment,
        # allow the patient to keep their current slot.
        if appointment:
            available_slots = (
                AppointmentSlot.objects.filter(
                    date__gte=today
                )
                .filter(
                    models.Q(
                        appointments__status__isnull=True
                    )
                    | models.Q(
                        appointments__status="cancelled"
                    )
                    | models.Q(
                        id=appointment.slot_id
                    )
                )
                .select_related("doctor")
                .distinct()
                .order_by("date", "start_time")
            )

        self.fields["slot"].queryset = available_slots

        self.fields["slot"].label = "Available appointment slot"
        self.fields["reason"].label = "Reason for appointment"

    def clean_slot(self):
        slot = self.cleaned_data["slot"]

        confirmed_exists = Appointment.objects.filter(
            slot=slot,
            status="confirmed"
        )

        if self.appointment:
            confirmed_exists = confirmed_exists.exclude(
                id=self.appointment.id
            )

        if confirmed_exists.exists():
            raise forms.ValidationError(
                "This appointment slot has already been booked."
            )

        return slot

    def clean_reason(self):
        reason = self.cleaned_data["reason"].strip()

        if len(reason) < 5:
            raise forms.ValidationError(
                "Please provide at least 5 characters describing the reason."
            )

        return reason