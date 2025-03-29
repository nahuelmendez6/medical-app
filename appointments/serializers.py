from rest_framework import serializers

from users.models import PatientProfile, DoctorProfile
from .models import Appointments

class AppointMentSerializer(serializers.Serializer):

    patient = serializers.PrimaryKeyRelatedField(queryset=PatientProfile.objects.all())
    doctor = serializers.PrimaryKeyRelatedField(queryset=DoctorProfile.objects.all())
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

    def create(self, validate_data):
        patient_instance = validate_data.pop('patient')
        doctor_instance = validate_data.pop('doctor')

        appointment = Appointments.objects.create(
            patient = patient_instance,
            doctor = doctor_instance,
            status = validate_data['status'],
            date = validate_data['date'],
            start_time = validate_data['start_time'],
            end_time = validate_data['end_time']
        )

        return appointment

