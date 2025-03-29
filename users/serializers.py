from django.db.models import IntegerField
from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, AuthUser
from rest_framework_simplejwt.tokens import Token

User = get_user_model()

from .models import CustomUser, DoctorProfile, DoctorSchedule, PatientProfile


class RegisterSerializer(serializers.Serializer):

    first_name = serializers.CharField(
        max_length=150,
        required=True
    )

    last_name = serializers.CharField(
        max_length=150,
        required=True
    )

    dni_number = serializers.CharField(
        max_length=10,
        required=True
    )

    username = serializers.CharField(
        max_length=150,
        required=True,
        help_text='Requerido. 150 caracteres o menos'
    )

    email = serializers.EmailField(
        required=True,
        help_text='Requerido. Ingrese un mail válido'
    )

    password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=8,
        help_text='La contraseña debe tener al menos 8 caracteres'
    )

    password2 = serializers.CharField(
        write_only=True,
        required=True,
        help_text="Repita la contraseña para verificacion"
    )

    role = serializers.ChoiceField(
        choices=User.ROLE_CHOICES,
        default='patient'
    )

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Este nombre de usuario ya existe")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este correo electronico ya existe")
        return value

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password': 'Las contraseñas no coinciden'})
        return data

    def create(self, validated_data):
        # Crear y devolver un nuevo usuario

        validated_data.pop('password2')

        user = User.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            dni_number=validated_data['dni_number'],
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role']
        )

        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role
        return token


class DoctorProfileSerializer(serializers.Serializer):

    user = serializers.IntegerField()
    specialty = serializers.ChoiceField(
        choices=DoctorProfile.SPECIALTY_CHOICES
    )
    license_number = serializers.CharField(
        max_length=10
    )
    consultation_fee = serializers.DecimalField(
        max_digits=10,  # Permite hasta 99999999.99
        decimal_places=2,
    )

    def create(self, validated_data):
        user_id = validated_data.pop('user')
        user_instance = CustomUser.objects.get(id=user_id)
        doctor_profile = DoctorProfile.objects.create(
            user = user_instance,
            specialty = validated_data['specialty'],
            license_number = validated_data['license_number'],
            consultation_fee = validated_data['consultation_fee']
        )

        return doctor_profile


class DoctorScheduleSerializer(serializers.Serializer):

    doctor = serializers.IntegerField()
    day = serializers.ChoiceField(
        choices=DoctorSchedule.DAY_CHOICES
    )
    start_time = serializers.TimeField(format='%H:%M')
    end_time = serializers.TimeField(format='%H:%M')

    def validate_times(self, data):
        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError({'end_time':'El horario de finalización debe ser posterio al horario de '
                                                          'comienzo'})
        return data

    def create(self, validated_data):

        doctor_schedule = DoctorSchedule.objects.create(
            doctor = validated_data['doctor'],
            day = validated_data['day'],
            start_time = validated_data['start_time'],
            end_time = validated_data['end_time']
        )

        return doctor_schedule


class PatientProfileSerializer(serializers.Serializer):

    user = IntegerField()

    def create(self, validated_data):

        patient_profile = PatientProfile.objects.create(
            user = validated_data['user']
        )

        return patient_profile