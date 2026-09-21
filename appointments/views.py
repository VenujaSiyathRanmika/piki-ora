from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import Patient
from .forms import AppointmentForm
from .models import Appointment


def get_patient(request):
    return get_object_or_404(
        Patient,
        user=request.user
    )


@login_required
def book_appointment(request):
    patient = get_patient(request)

    if request.method == "POST":
        form = AppointmentForm(request.POST)

        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = patient
            appointment.status = "confirmed"

            try:
                with transaction.atomic():
                    appointment.save()

                messages.success(
                    request,
                    "Your appointment has been booked successfully."
                )

                return redirect("my_appointments")

            except IntegrityError:
                messages.error(
                    request,
                    "Sorry, that appointment slot has just been booked by another patient."
                )
    else:
        form = AppointmentForm()

    return render(
        request,
        "appointments/book_appointment.html",
        {
            "form": form,
        }
    )


@login_required
def my_appointments(request):
    patient = get_patient(request)

    appointments = (
        Appointment.objects
        .filter(patient=patient)
        .select_related("slot", "slot__doctor")
        .order_by(
            "-slot__date",
            "-slot__start_time"
        )
    )

    return render(
        request,
        "appointments/my_appointments.html",
        {
            "appointments": appointments,
        }
    )


@login_required
def edit_appointment(request, appointment_id):
    patient = get_patient(request)

    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        patient=patient,
        status="confirmed",
    )

    if request.method == "POST":
        form = AppointmentForm(
            request.POST,
            instance=appointment,
            appointment=appointment,
        )

        if form.is_valid():
            try:
                with transaction.atomic():
                    form.save()

                messages.success(
                    request,
                    "Your appointment has been updated successfully."
                )

                return redirect("my_appointments")

            except IntegrityError:
                messages.error(
                    request,
                    "That appointment slot is no longer available."
                )
    else:
        form = AppointmentForm(
            instance=appointment,
            appointment=appointment,
        )

    return render(
        request,
        "appointments/edit_appointment.html",
        {
            "form": form,
            "appointment": appointment,
        }
    )


@login_required
def cancel_appointment(request, appointment_id):
    patient = get_patient(request)

    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        patient=patient,
        status="confirmed",
    )

    if request.method == "POST":
        appointment.status = "cancelled"
        appointment.save()

        messages.success(
            request,
            "Your appointment has been cancelled."
        )

        return redirect("my_appointments")

    return render(
        request,
        "appointments/cancel_appointment.html",
        {
            "appointment": appointment,
        }
    )