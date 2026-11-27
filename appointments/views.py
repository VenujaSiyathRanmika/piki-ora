
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.models import Patient
from .forms import AppointmentForm
from .models import Appointment, AppointmentSlot
from .serializers import AppointmentSerializer, AppointmentSlotSerializer


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
                    "Appointment booked successfully."
                )

                return redirect("my_appointments")

            except IntegrityError:
                messages.error(
                    request,
                    "This slot is already booked."
                )
    else:
        form = AppointmentForm()

    return render(
        request,
        "appointments/book_appointment.html",
        {"form": form}
    )


@login_required
def my_appointments(request):
    patient = get_patient(request)

    appointments = Appointment.objects.filter(
        patient=patient
    ).select_related("slot", "slot__doctor")

    return render(
        request,
        "appointments/my_appointments.html",
        {"appointments": appointments}
    )


@login_required
def edit_appointment(request, appointment_id):
    patient = get_patient(request)

    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        patient=patient,
        status="confirmed"
    )

    if request.method == "POST":
        form = AppointmentForm(
            request.POST,
            instance=appointment,
            appointment=appointment
        )

        if form.is_valid():
            try:
                with transaction.atomic():
                    form.save()

                messages.success(
                    request,
                    "Appointment updated successfully."
                )

                return redirect("my_appointments")

            except IntegrityError:
                messages.error(
                    request,
                    "This slot is already booked."
                )
    else:
        form = AppointmentForm(
            instance=appointment,
            appointment=appointment
        )

    return render(
        request,
        "appointments/edit_appointment.html",
        {
            "form": form,
            "appointment": appointment
        }
    )


@login_required
def cancel_appointment(request, appointment_id):
    patient = get_patient(request)

    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        patient=patient,
        status="confirmed"
    )

    if request.method == "POST":
        appointment.status = "cancelled"
        appointment.save()

        messages.success(
            request,
            "Appointment cancelled."
        )

        return redirect("my_appointments")

    return render(
        request,
        "appointments/cancel_appointment.html",
        {"appointment": appointment}
    )


@api_view(["GET"])
def appointment_slot_list(request):
    slots = AppointmentSlot.objects.filter(
        date__gte=timezone.localdate()
    ).select_related("doctor")

    serializer = AppointmentSlotSerializer(
        slots,
        many=True
    )

    return Response(serializer.data)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def appointment_list(request):

    if request.user.is_staff:
        if request.method == "GET":
            appointments = Appointment.objects.all().select_related(
                "patient",
                "slot",
                "slot__doctor"
            )

            serializer = AppointmentSerializer(
                appointments,
                many=True
            )

            return Response(serializer.data)

        return Response(
            {
                "error": "Admins cannot create appointments using this API."
            },
            status=status.HTTP_403_FORBIDDEN
        )

    patient = get_patient(request)

    if request.method == "GET":
        appointments = Appointment.objects.filter(
            patient=patient
        ).select_related(
            "slot",
            "slot__doctor"
        )

        serializer = AppointmentSerializer(
            appointments,
            many=True
        )

        return Response(serializer.data)

    serializer = AppointmentSerializer(
        data=request.data
    )

    if serializer.is_valid():
        try:
            with transaction.atomic():
                serializer.save(
                    patient=patient,
                    status="confirmed"
                )

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        except IntegrityError:
            return Response(
                {
                    "error": "This slot is already booked."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def cancel_appointment_api(request, appointment_id):

    if request.user.is_staff:
        appointment = get_object_or_404(
            Appointment,
            id=appointment_id,
            status="confirmed"
        )
    else:
        patient = get_patient(request)

        appointment = get_object_or_404(
            Appointment,
            id=appointment_id,
            patient=patient,
            status="confirmed"
        )

    appointment.status = "cancelled"
    appointment.save()

    return Response({
        "message": "Appointment cancelled successfully."
    })
