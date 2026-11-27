from rest_framework import serializers
from .models import AppointmentSlot, Appointment


class AppointmentSlotSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(
        source="doctor.__str__",
        read_only=True
    )

    class Meta:
        model = AppointmentSlot
        fields = [
            "id",
            "doctor",
            "doctor_name",
            "date",
            "start_time",
            "end_time",
        ]


class AppointmentSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(
        source="slot.doctor.__str__",
        read_only=True
    )

    date = serializers.DateField(
        source="slot.date",
        read_only=True
    )

    start_time = serializers.TimeField(
        source="slot.start_time",
        read_only=True
    )

    end_time = serializers.TimeField(
        source="slot.end_time",
        read_only=True
    )

    class Meta:
        model = Appointment
        fields = [
            "id",
            "patient",
            "slot",
            "doctor_name",
            "date",
            "start_time",
            "end_time",
            "reason",
            "status",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "patient",
            "status",
            "created_at",
        ]
