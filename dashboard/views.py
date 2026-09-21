from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from accounts.models import Patient
from appointments.models import Appointment


@login_required
def patient_dashboard(request):

    # Staff/admin users should use the custom administrator dashboard.
    if request.user.is_staff:
        return redirect("admin_dashboard")

    patient = get_object_or_404(
        Patient,
        user=request.user
    )

    today = timezone.localdate()

    upcoming_appointments = (
        Appointment.objects
        .filter(
            patient=patient,
            status="confirmed",
            slot__date__gte=today,
        )
        .select_related(
            "slot",
            "slot__doctor",
        )
        .order_by(
            "slot__date",
            "slot__start_time",
        )
    )

    next_appointment = upcoming_appointments.first()

    recent_appointments = (
        Appointment.objects
        .filter(
            patient=patient
        )
        .select_related(
            "slot",
            "slot__doctor",
        )
        .order_by(
            "-created_at"
        )[:5]
    )

    context = {
        "patient": patient,
        "next_appointment": next_appointment,
        "recent_appointments": recent_appointments,
    }

    return render(
        request,
        "dashboard/patient_dashboard.html",
        context
    )