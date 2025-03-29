from rest_framework import serializers
from .models import Appointments, AppointmentSchedule

class AppointMentSerializer(serializers.Serializer):

    patient = serializers.IntegerField()
    doctor = serializers.IntegerField()
    status = serializers.ChoiceField(
        choices=Appointments.STATUS_CHOICES
    )

    def validate(self, data):
        overlapping = AppointmentsSchedule.objects.filter(

        )
