from celery import shared_task
from django.core.mail import send_mail, EmailMultiAlternatives

from django.conf import settings
from django.template.loader import render_to_string


@shared_task
def send_appointment_email_task(email, context):
    subject = 'Recordatorio de cita medica'
    from_email = settings.DEFAULT_FROM_EMAIL
    to = [email]

    html_content = render_to_string('emails/appointment_reminder.html', context)
    text_content = f"Tenés una cita el {context['date']} a las {context['start_time']} con el Dr./Dra. {context['doctor_name']}."

    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def send_doctor_appointment_task(email, context):
    subject = 'Nueva cita'
    from_email = settings.DEFAULT_FROM_EMAIL
    to = [email]

    html_content = render_to_string('emails/appointment_doctor_reminder.html', context)
    text_content = f"Tenés una cita el {context['date']} a las {context['start_time']} con el Sr./Sra. {context['name']}."

    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
