from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import CreateAppointmentView

urlpatterns = {
    path('new/', CreateAppointmentView.as_view(), name='create_appointment')
}
