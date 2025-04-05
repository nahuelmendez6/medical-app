from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from users.models import CustomUser
from users.permissions import IsPatient, IsDoctor, IsAdmin
from .serializers import AppointMentSerializer
from .tasks import send_appointment_email_task
# Create your views here.

class CreateAppointmentView(APIView):

    permission_classes = [IsAuthenticated]
    """
    Endpoint para registar una cita
    """
    def post(self, request):
        serializer = AppointMentSerializer(data=request.data)
        if serializer.is_valid():
            appointment = serializer.save()

            user_id = appointment.patient.user_id
            doctor_id = appointment.doctor.user_id
            user_doctor = CustomUser.objects.get(id=doctor_id)
            user_patient = CustomUser.objects.get(id=user_id)

            email = user_patient.email

            message = (f"Hola {user_patient.first_name}, tu cita con {appointment.doctor.user.username} ha sido programada "
                       f"para el {appointment.date} a las {appointment.start_time}.")

            send_appointment_email_task.delay(
                email=email,
                context={
                    'name': user_patient.username,
                    'date': appointment.date.strftime('%d%m%Y'),
                    'start_time': appointment.start_time.strftime('%H:%M'),
                    'doctor_name': user_doctor.username,
                }
            )

            return Response(
                {'message':'Cita creada exitosamente'},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)