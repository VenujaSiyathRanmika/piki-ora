from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from .models import Appointment, AppointmentSlot
from doctors.models import Doctor
from .serializers import AppointmentSerializer, AppointmentSlotSerializer


@api_view(["GET"])
@permission_classes([IsAdminUser])
def admin_appointments(request):
    appointments = Appointment.objects.select_related(
        "patient__user", "slot__doctor"
    ).order_by("-slot__date", "-slot__start_time")

    return Response(AppointmentSerializer(appointments, many=True).data)


@api_view(["GET", "POST"])
@permission_classes([IsAdminUser])
def admin_doctors(request):
    if request.method == "GET":
        doctors = Doctor.objects.all().order_by("first_name")
        data = [
            {
                "id": d.id,
                "first_name": d.first_name,
                "last_name": d.last_name,
                "specialisation": d.specialisation,
                "email": d.email,
                "phone": d.phone,
                "bio": d.bio,
            }
            for d in doctors
        ]
        return Response(data)

    data = request.data
    required = ["first_name", "last_name", "specialisation", "email"]
    if any(not data.get(field) for field in required):
        return Response(
            {"error": "First name, last name, specialisation and email are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    doctor = Doctor.objects.create(
        first_name=data["first_name"],
        last_name=data["last_name"],
        specialisation=data["specialisation"],
        email=data["email"],
        phone=data.get("phone", ""),
        bio=data.get("bio", ""),
    )
    return Response(
        {"id": doctor.id, "message": "Doctor created successfully."},
        status=status.HTTP_201_CREATED,
    )


@api_view(["GET", "POST"])
@permission_classes([IsAdminUser])
def admin_slots(request):
    if request.method == "GET":
        slots = AppointmentSlot.objects.select_related("doctor").order_by(
            "date", "start_time"
        )
        return Response(AppointmentSlotSerializer(slots, many=True).data)

    data = request.data
    required = ["doctor", "date", "start_time", "end_time"]
    if any(not data.get(field) for field in required):
        return Response(
            {"error": "Doctor, date, start time and end time are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    slot = AppointmentSlot.objects.create(
        doctor_id=data["doctor"],
        date=data["date"],
        start_time=data["start_time"],
        end_time=data["end_time"],
    )
    return Response(
        {"id": slot.id, "message": "Appointment slot created successfully."},
        status=status.HTTP_201_CREATED,
    )
