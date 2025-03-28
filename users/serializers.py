from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, AuthUser
from rest_framework_simplejwt.tokens import Token

User = get_user_model()

from .models import CustomUser


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