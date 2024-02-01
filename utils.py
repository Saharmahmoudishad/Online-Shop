from django.core.cache import cache
from django.utils.crypto import get_random_string
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from customers.tasks import send_email_task
from config import settings
from kavenegar import *
from config.settings import config


def generate_and_store_otp(phone_or_email):
    """Create random code and cache it"""
    cache_key = phone_or_email
    cached_data = cache.get(cache_key)
    if cached_data is not None:
        return cached_data['otp_code']
    else:
        otp_code = get_random_string(length=6, allowed_chars="0123456789")
        data_to_cache = {"otp_code": otp_code}
        cache.set(cache_key, data_to_cache, timeout=259200)
    return otp_code


def send_otpcode_email(email, otp_code):
    """send random code to email address"""
    subject = 'Account activation'
    html_message = render_to_string('customers/active_code.html', {'otp_code': otp_code})
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to_email = [email]
    send_email_task.delay(subject, plain_message, from_email, to_email, html_message=html_message)


def send_registration_email(email, uidb64, token_generator, protocol, domain):
    """send link of registeration to email address"""
    subject = 'Account activation'
    html_message = render_to_string('customers/confirm_authentication.html', {'email': email, 'uidb64': uidb64,
                                                                              'token': token_generator,
                                                                              'protocol': protocol, 'domain': domain})
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to_email = [email]
    send_email_task.delay(subject, plain_message, from_email, to_email, html_message=html_message)


def kave_negar_token_send(receptor, token):
    """send random code to phone number"""
    APIKey = config.get('sending_sms', 'APIKey')
    try:
        api = KavenegarAPI(APIKey)
        params = {
            'receptor': receptor,
            'template':'verify',
            'token': token,}
        response = api.verify_lookup(params)
        print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)
