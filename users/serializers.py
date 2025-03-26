from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()

from .models import CustomUser


def validate_email(value):
    if User.objects.filter(email=value).exists():
        raise serializers.ValidationError("Este correo electronico ya existe")
    return value


class RegisterSerializer(serializers.Serializer):

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

        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password': 'Las contraseñas no coinciden'})
        return data