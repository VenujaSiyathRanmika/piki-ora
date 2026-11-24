
from django.db import IntegrityError, transaction
from django.utils import timezone

from rest_framework import status
from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Appointment, AppointmentSlot
from .serializers import (
    AppointmentSerializer,
    AppointmentSlotSerializer,
)


@api_view(["GET"])
def available_slots(request):
    slots = AppointmentSlot.objects.filter(
        date__gte=timezone.localdate()
    ).select_related("doctor").order_by(
        "date", "start_time"
    )

    serializer = AppointmentSlotSerializer(
        slots,
        many=True
    )

    return Response(serializer.data)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def patient_appointments(request):
    try:
        patient = request.user.patient_profile
    except Exception:
        return Response(
            {"error": "A patient profile is required."},
            status=status.HTTP_403_FORBIDDEN
        )

    if request.method == "GET":
        appointments = Appointment.objects.filter(
            patient=patient
        ).select_related(
            "slot__doctor",
            "patient__user"
        )

        serializer = AppointmentSerializer(
            appointments,
            many=True
        )

        return Response(serializer.data)

    slot_id = request.data.get("slot")
    reason = request.data.get("reason", "").strip()

    if not slot_id or not reason:
        return Response(
            {"error": "Please select a slot and enter a reason."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        with transaction.atomic():
            slot = AppointmentSlot.objects.select_for_update().get(
                id=slot_id
            )

            if slot.date < timezone.localdate():
                return Response(
                    {"error": "This appointment date has passed."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if Appointment.objects.filter(
                slot=slot,
                status="confirmed"
            ).exists():
                return Response(
                    {"error": "This slot is already booked."},
                    status=status.HTTP_409_CONFLICT
                )

            appointment = Appointment.objects.create(
                patient=patient,
                slot=slot,
                reason=reason,
                status="confirmed"
            )

    except AppointmentSlot.DoesNotExist:
        return Response(
            {"error": "Appointment slot not found."},
            status=status.HTTP_404_NOT_FOUND
        )
    except IntegrityError:
        return Response(
            {"error": "This slot has already been booked."},
            status=status.HTTP_409_CONFLICT
        )

    serializer = AppointmentSerializer(appointment)

    return Response(
        serializer.data,
        status=status.HTTP_201_CREATED
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def cancel_appointment_api(request, appointment_id):
    try:
        patient = request.user.patient_profile
    except Exception:
        return Response(
            {"error": "A patient profile is required."},
            status=status.HTTP_403_FORBIDDEN
        )

    try:
        appointment = Appointment.objects.get(
            id=appointment_id,
            patient=patient,
            status="confirmed"
        )
    except Appointment.DoesNotExist:
        return Response(
            {"error": "Appointment not found."},
            status=status.HTTP_404_NOT_FOUND
        )

    appointment.status = "cancelled"
    appointment.save()

    return Response(
        {"message": "Appointment cancelled successfully."},
        status=status.HTTP_200_OK
    )
