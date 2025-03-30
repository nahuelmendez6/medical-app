from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_appointment_notification(email, message):
    send_mail(
        subject="Recordatorio de cita",
        message=message,
        from_email="no-reply@medicalapp.com",
        recipient_list=[email],
    )