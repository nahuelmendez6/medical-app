from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db.models import CASCADE


# Create your models here.

class CustomUser(AbstractUser):

    ROLE_CHOICES = [
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('admin', 'Admin'),
    ]
    first_name = models.CharField(max_length=150, null=False)
    last_name = models.CharField(max_length=150, null=False)
    dni_number = models.CharField(max_length=8, null=False)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='patient')
    email = models.EmailField(('email address'), unique=True)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message='El formato de celular debe ser +9999999999'
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17,
        blank=True
    )

    # Metodos de permisos
    @property
    def is_patient(self):
        """ Retorna true si el usuario es paciente """
        return self.role == 'patient'

    @property
    def is_doctor(self):
        """ Retorna true si el usuario es doctor """
        return self.role == 'doctor'

    @property
    def is_admin(self):
        return self.role == 'admin'

    class Meta:
        verbose_name = ('Usuario')
        verbose_name_plural = ('Usuarios')
        ordering = ['-date_joined']
        db_table = 'custom_users'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['role'])
        ]


class DoctorProfile(models.Model):

    SPECIALTY_CHOICES = [
        ('cardiologia', 'Cardiología'),
        ('odontología', 'Odontología'),
        ('oftalmología', 'Oftalmología')
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='doctor_profile')
    specialty = models.CharField(max_length=25, choices=SPECIALTY_CHOICES, null=False)
    license_number = models.CharField(max_length=10, null=False)
    consultation_fee = models.DecimalField(
        max_digits=10,  # Permite hasta 99999999.99
        decimal_places=2,  # Dos decimales para valores monetarios
        null=False,
        default=0.00,  # Valor por defecto para evitar errores
    )

class DoctorSchedule(models.Model):

    DAY_CHOICES = [
        ('monday', 'Lunes'),
        ('tuesday', 'Martes'),
        ('wednesday', 'Miercoles'),
        ('thursday', 'Jueves'),
        ('friday', 'Viernes')
    ]

    HOUR_CHOICES = [
        ("08:00", "08:00 AM"), ("08:30", "08:30 AM"),
        ("09:00", "09:00 AM"), ("09:30", "09:30 AM"),
        ("10:00", "10:00 AM"), ("10:30", "10:30 AM"),
        ("11:00", "11:00 AM"), ("11:30", "11:30 AM"),
        ("12:00", "12:00 PM"), ("12:30", "12:30 PM"),
        ("13:00", "01:00 PM"), ("13:30", "01:30 PM"),
        ("14:00", "02:00 PM"), ("14:30", "02:30 PM"),
        ("15:00", "03:00 PM"), ("15:30", "03:30 PM"),
        ("16:00", "04:00 PM"), ("16:30", "04:30 PM"),
        ("17:00", "05:00 PM"), ("17:30", "05:30 PM"),
        ("18:00", "06:00 PM"), ("18:30", "06:30 PM"),
        ("19:00", "07:00 PM"), ("19:30", "07:30 PM"),
        ("20:00", "08:00 PM"), ("20:30", "08:30 PM")
    ]

    doctor = models.ForeignKey(DoctorProfile, on_delete=CASCADE, related_name='doctor_schedule')
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()


class PatientProfile(models.Model):

    user = models.OneToOneField(CustomUser, on_delete=CASCADE, related_name='patient_profile')
