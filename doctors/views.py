
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from .models import Doctor
from .serializers import DoctorSerializer


@api_view(["GET"])
def doctor_list_api(request):
    doctors = Doctor.objects.all()
    serializer = DoctorSerializer(doctors, many=True)

    response = Response(serializer.data)
    response.accepted_renderer = JSONRenderer()
    response.accepted_media_type = "application/json"
    response.renderer_context = {}

    return response
