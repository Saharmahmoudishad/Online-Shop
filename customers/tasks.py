from django.core.mail import send_mail
from celery import shared_task


@shared_task
def send_email_task(subject, message, from_email, recipient_list, html_message):
    send_mail(subject, message, from_email, recipient_list, html_message)
