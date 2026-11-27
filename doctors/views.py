from rest_framework.decorators import api_view
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from .models import Doctor
from .serializers import DoctorSerializer


@api_view(["GET"])
def doctor_list(request):
    doctors = Doctor.objects.all()
    serializer = DoctorSerializer(doctors, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def add_doctor(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return Response(
            {"error": "Admin login required."},
            status=status.HTTP_403_FORBIDDEN
        )

    serializer = DoctorSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(["PUT"])
def edit_doctor(request, doctor_id):
    if not request.user.is_authenticated or not request.user.is_staff:
        return Response(
            {"error": "Admin login required."},
            status=status.HTTP_403_FORBIDDEN
        )

    try:
        doctor = Doctor.objects.get(id=doctor_id)
    except Doctor.DoesNotExist:
        return Response(
            {"error": "Doctor not found."},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = DoctorSerializer(
        doctor,
        data=request.data
    )

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(["DELETE"])
def delete_doctor(request, doctor_id):
    if not request.user.is_authenticated or not request.user.is_staff:
        return Response(
            {"error": "Admin login required."},
            status=status.HTTP_403_FORBIDDEN
        )

    try:
        doctor = Doctor.objects.get(id=doctor_id)
    except Doctor.DoesNotExist:
        return Response(
            {"error": "Doctor not found."},
            status=status.HTTP_404_NOT_FOUND
        )

    doctor.delete()

    return Response(
        {"message": "Doctor deleted successfully."},
        status=status.HTTP_200_OK
    )
