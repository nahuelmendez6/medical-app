from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .serializers import AppointMentSerializer
# Create your views here.

class CreateAppointmentView(APIView):

    permission_classes = [AllowAny]
    """
    Endpoint para registar una cita
    """
    def post(self, request):
        serializer = AppointMentSerializer(data=request.data)
        if serializer.is_valid():
            appointment = serializer.save()
            return Response(
                {'message':'Cita creada exitosamente'},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)