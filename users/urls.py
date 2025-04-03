from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (RegisterView, CustomTokenObtainPairView, CreateDoctorProfileView, CreateDoctorScheduleView,
                    CreatePatientProfileView, LoginView)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/profile/doctor', CreateDoctorProfileView.as_view(), name='doctor_profile'),
    path('register/schedule/doctor', CreateDoctorScheduleView.as_view(), name='doctor_schedule'),
    path('register/patient/profile', CreatePatientProfileView.as_view(), name='patient_profile')
]