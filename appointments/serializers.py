from rest_framework import serializers
from .models import Appointments

class AppointMentSerializer(serializers.Serializer):

    patient = serializers.IntegerField()
    doctor = serializers.IntegerField()
    status = serializers.ChoiceField(
        choices=Appointments.STATUS_CHOICES
    )
    date = serializers.DateField()
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()

    def validate(self, data):
        overlapping = Appointments.objects.filter(
            doctor = data['doctor'],
            status = data['status'],
            date = data['date'],
            start_time = data['start_time']
        )
        if overlapping:
            raise serializers.ValidationError('Fecha y horario para consulta ya ocupado')

        return data

