from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_email(subject,message,recipient_list):
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=recipient_list
    )