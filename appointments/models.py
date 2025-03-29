from django.db import models
from django.db.models import UniqueConstraint

from users.models import CustomUser, DoctorProfile, PatientProfile


# Create your models here.


class Appointments(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pendiente'),
        ('confirmed', 'Confirmado'),
        ('cancelled', 'Candelada'),
        ('completed', 'Completada')
    )
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='appointments_patient')
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='appointments_doctor')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    class Meta:
        constraints = [
            UniqueConstraint(fields=['doctor', 'date', 'start_time'], name='unique_appointment')
        ]

class AppointmentSchedule(models.Model):

    appointment = models.ForeignKey(Appointments, on_delete=models.CASCADE, related_name='appointment_date')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
