from datetime import timedelta

from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail
from celery import shared_task
from django.utils import timezone

from config import settings
from core.models import DiscountCode
from customers.models import CustomUser


@shared_task
def send_email_task(subject, message, from_email, recipient_list, html_message):
    send_mail(subject, message, from_email, recipient_list, html_message)

@shared_task
def employee_gift_discount_code():
    staffs = CustomUser.objects.filter(is_admin=True)

    for staff in staffs:
        discount_code = DiscountCode.objects.create(
            amount=0.2,
            deadline=timezone.now() + timedelta(days=365),
            content_type=ContentType.objects.get_for_model(CustomUser),
            object_id=staff.id,
            statusCharge=10)
        subject = "Employee gift, Discount Code Notification"
        message = f"Dear {staff.firstname} {staff.lastname},\n\nYou have received a discount code: {discount_code.title}\n\nDeadline: {discount_code.deadline}\n\nAmount: {discount_code.amount}\n\n, On the anniversary of the establishment of the store."
        from_email = settings.EMAIL_HOST_USER
        to_email = [staff.email]
        send_mail(subject, message, from_email, to_email)

