from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework import viewsets, generics, status
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.views import TokenObtainPairView
from django.utils import timezone
from datetime import timedelta

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import RegisterSerializer, CustomTokenObtainPairSerializer
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