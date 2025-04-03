from django.shortcuts import render
from django.template.context_processors import request
from rest_framework.decorators import action
from rest_framework import viewsets, generics, status
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.utils import timezone
from datetime import timedelta

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import DoctorProfile
from users.serializers import (RegisterSerializer, CustomTokenObtainPairSerializer, DoctorProfileSerializer,
                               DoctorScheduleSerializer, PatientProfileSerializer, LoginSerializer)
# Create your views here.

class RegisterView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        """
        Endpoint para registrar a un nuevo usuario
        """
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {'message': 'Usuario registrado existosamente'},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh':str(refresh),
                'access':str(refresh.access_token),
                'user':{
                    'id':user.id,
                    'first_name':user.first_name,
                    'last_name':user.last_name,
                    'dni_number':user.dni_number,
                    'role':user.role,
                    'email':user.email,
                    'phone_number':user.phone_number
                }
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateDoctorProfileView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        """
        Endpoint para completar el perfil de un doctor
        """
        serializer = DoctorProfileSerializer(data=request.data)
        if serializer.is_valid():
            doctor_profile = serializer.save()
            return Response(
                {'message':'Perfil guardado existosamente'},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateDoctorScheduleView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = DoctorScheduleSerializer(data=request.data)
        if serializer.is_valid():
            doctor_schedule = serializer.save()
            return Response(
                {'message': 'Disponibilidad guardada existosamente'},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreatePatientProfileView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PatientProfileSerializer(data=request.data)
        if serializer.is_valid():
            patient_profile = serializer.save()
            return Response(
                {'message': 'Perfil guardado existosamente'},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)