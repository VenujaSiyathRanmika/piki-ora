
from rest_framework import serializers
from .models import AppointmentSlot, Appointment


class AppointmentSlotSerializer(serializers.ModelSerializer):
    doctor_name = serializers.SerializerMethodField()
    specialisation = serializers.CharField(
        source="doctor.specialisation",
        read_only=True
    )
    is_available = serializers.SerializerMethodField()

    class Meta:
        model = AppointmentSlot
        fields = [
            "id",
            "doctor",
            "doctor_name",
            "specialisation",
            "date",
            "start_time",
            "end_time",
            "is_available",
        ]

    def get_doctor_name(self, obj):
        return (
            f"Dr. {obj.doctor.first_name} "
            f"{obj.doctor.last_name}"
        )

    def get_is_available(self, obj):
        return not obj.appointments.filter(
            status="confirmed"
        ).exists()


class AppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.SerializerMethodField()
    slot_details = AppointmentSlotSerializer(
        source="slot",
        read_only=True
    )

    class Meta:
        model = Appointment
        fields = [
            "id",
            "patient",
            "patient_name",
            "slot",
            "slot_details",
            "reason",
            "status",
            "created_at",
        ]
        read_only_fields = [
            "patient",
            "status",
            "created_at",
        ]

    def get_patient_name(self, obj):
        return (
            f"{obj.patient.user.first_name} "
            f"{obj.patient.user.last_name}"
        )
