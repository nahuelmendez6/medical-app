from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, CustomTokenObtainPairView, CreateDoctorProfileView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register')
]