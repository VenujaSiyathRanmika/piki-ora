from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import Patient
from appointments.models import Appointment, AppointmentSlot
from doctors.models import Doctor

from .forms import (
    AdminAppointmentForm,
    AppointmentSlotForm,
    DoctorForm,
)


User = get_user_model()


def is_staff_user(user):
    return user.is_authenticated and user.is_staff


staff_required = user_passes_test(
    is_staff_user,
    login_url="/accounts/admin-login/",
)


@staff_required
def admin_dashboard(request):
    total_doctors = Doctor.objects.count()
    total_slots = AppointmentSlot.objects.count()

    total_appointments = Appointment.objects.count()

    confirmed_appointments = Appointment.objects.filter(
        status="confirmed"
    ).count()

    total_patients = Patient.objects.count()

    recent_appointments = (
        Appointment.objects
        .select_related(
            "patient",
            "patient__user",
            "slot",
            "slot__doctor",
        )
        .order_by("-created_at")[:8]
    )

    context = {
        "total_doctors": total_doctors,
        "total_slots": total_slots,
        "total_appointments": total_appointments,
        "confirmed_appointments": confirmed_appointments,
        "total_patients": total_patients,
        "recent_appointments": recent_appointments,
    }

    return render(
        request,
        "dashboard/admin_dashboard.html",
        context,
    )


@staff_required
def doctor_list(request):
    doctors = Doctor.objects.all().order_by(
        "last_name",
        "first_name",
    )

    return render(
        request,
        "dashboard/doctors.html",
        {
            "doctors": doctors,
        },
    )


@staff_required
def doctor_create(request):
    if request.method == "POST":
        form = DoctorForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Doctor added successfully.",
            )

            return redirect("admin_doctors")

    else:
        form = DoctorForm()

    return render(
        request,
        "dashboard/doctor_form.html",
        {
            "form": form,
            "title": "Add Doctor",
            "button_text": "Add Doctor",
        },
    )


@staff_required
def doctor_edit(request, doctor_id):
    doctor = get_object_or_404(
        Doctor,
        id=doctor_id,
    )

    if request.method == "POST":
        form = DoctorForm(
            request.POST,
            instance=doctor,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Doctor updated successfully.",
            )

            return redirect("admin_doctors")

    else:
        form = DoctorForm(
            instance=doctor,
        )

    return render(
        request,
        "dashboard/doctor_form.html",
        {
            "form": form,
            "title": "Edit Doctor",
            "button_text": "Save Changes",
        },
    )


@staff_required
def doctor_delete(request, doctor_id):
    doctor = get_object_or_404(
        Doctor,
        id=doctor_id,
    )

    if request.method == "POST":
        doctor.delete()

        messages.success(
            request,
            "Doctor deleted successfully.",
        )

        return redirect("admin_doctors")

    return render(
        request,
        "dashboard/doctor_delete.html",
        {
            "doctor": doctor,
        },
    )


@staff_required
def slot_list(request):
    slots = (
        AppointmentSlot.objects
        .select_related("doctor")
        .prefetch_related("appointments")
        .order_by(
            "date",
            "start_time",
        )
    )

    return render(
        request,
        "dashboard/slots.html",
        {
            "slots": slots,
        },
    )


@staff_required
def slot_create(request):
    if request.method == "POST":
        form = AppointmentSlotForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Appointment slot created successfully.",
            )

            return redirect("admin_slots")

    else:
        form = AppointmentSlotForm()

    return render(
        request,
        "dashboard/slot_form.html",
        {
            "form": form,
            "title": "Create Appointment Slot",
            "button_text": "Create Slot",
        },
    )


@staff_required
def slot_edit(request, slot_id):
    slot = get_object_or_404(
        AppointmentSlot,
        id=slot_id,
    )

    if request.method == "POST":
        form = AppointmentSlotForm(
            request.POST,
            instance=slot,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Appointment slot updated successfully.",
            )

            return redirect("admin_slots")

    else:
        form = AppointmentSlotForm(
            instance=slot,
        )

    return render(
        request,
        "dashboard/slot_form.html",
        {
            "form": form,
            "title": "Edit Appointment Slot",
            "button_text": "Save Changes",
        },
    )


@staff_required
def slot_delete(request, slot_id):
    slot = get_object_or_404(
        AppointmentSlot,
        id=slot_id,
    )

    if request.method == "POST":
        slot.delete()

        messages.success(
            request,
            "Appointment slot deleted successfully.",
        )

        return redirect("admin_slots")

    return render(
        request,
        "dashboard/slot_delete.html",
        {
            "slot": slot,
        },
    )


@staff_required
def appointment_list(request):
    appointments = (
        Appointment.objects
        .select_related(
            "patient",
            "patient__user",
            "slot",
            "slot__doctor",
        )
        .order_by(
            "-created_at"
        )
    )

    return render(
        request,
        "dashboard/appointments.html",
        {
            "appointments": appointments,
        },
    )


@staff_required
def appointment_edit(request, appointment_id):
    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
    )

    if request.method == "POST":
        form = AdminAppointmentForm(
            request.POST,
            instance=appointment,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Appointment updated successfully.",
            )

            return redirect("admin_appointments")

    else:
        form = AdminAppointmentForm(
            instance=appointment,
        )

    return render(
        request,
        "dashboard/appointment_form.html",
        {
            "form": form,
            "appointment": appointment,
        },
    )


@staff_required
def patient_list(request):
    patients = (
        Patient.objects
        .select_related("user")
        .order_by(
            "user__last_name",
            "user__first_name",
        )
    )

    return render(
        request,
        "dashboard/patients.html",
        {
            "patients": patients,
        },
    )


@staff_required
def patient_toggle_status(request, patient_id):
    patient = get_object_or_404(
        Patient,
        id=patient_id,
    )

    if request.method == "POST":
        user = patient.user

        user.is_active = not user.is_active
        user.save()

        if user.is_active:
            messages.success(
                request,
                "Patient account has been activated.",
            )
        else:
            messages.success(
                request,
                "Patient account has been deactivated.",
            )

    return redirect("admin_patients")