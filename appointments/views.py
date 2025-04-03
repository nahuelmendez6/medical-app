from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from users.models import CustomUser
from users.permissions import IsPatient, IsDoctor, IsAdmin
from .serializers import AppointMentSerializer
from .tasks import send_appointment_notification
# Create your views here.

class CreateAppointmentView(APIView):

    permission_classes = [IsAuthenticated, IsPatient, IsAdmin]
    """
    Endpoint para registar una cita
    """
    def post(self, request):
        serializer = AppointMentSerializer(data=request.data)
        if serializer.is_valid():
            appointment = serializer.save()

            user_id = appointment.patient.user_id
            user_patient = CustomUser.objects.get(id=user_id)
            email = user_patient.email

            message = (f"Hola {user_patient.first_name}, tu cita con {appointment.doctor.user.username} ha sido programada "
                       f"para el {appointment.date} a las {appointment.start_time}.")

            send_appointment_notification(email, message)

            return Response(
                {'message':'Cita creada exitosamente'},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)