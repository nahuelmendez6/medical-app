from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
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