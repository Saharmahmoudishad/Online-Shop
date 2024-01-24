from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from config import settings
from kavenegar import *

from config.settings import config


def send_otpcode_email(email, otp_code):
    subject = 'Account activation'
    html_message = render_to_string('customers/active_code.html', {'otp_code': otp_code})
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to_email = [email]
    send_mail(subject, plain_message, from_email, to_email, html_message=html_message)


def send_registration_email(email, uidb64, token_generator, protocol, domain):
    subject = 'Account activation'
    html_message = render_to_string('customers/confirm_authentication.html', {'email': email, 'uidb64': uidb64,
                                                                              'token': token_generator,
                                                                              'protocol': protocol, 'domain': domain})
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to_email = [email]
    send_mail(subject, plain_message, from_email, to_email, html_message=html_message)


def kave_negar_token_send(receptor, token):
    print("1" * 60, "saraaaa")
    APIKey = config.get('sending_sms', 'APIKey')
    try:
        api = KavenegarAPI(APIKey)
        params = {
            'sender': '',
            'receptor': receptor,
            'message': f'کد تایید ثبت نام شما {token} تست واحد فنی_ DroomBT.ir', }

        response = api.sms_send(params)
        print(response)
    except APIException as e:
        print(e)
        print(e)
    except HTTPException as e:
        print(e)
        print(e)


def generate_and_store_otp(phone_or_email):
    cache_key = phone_or_email
    cached_data = cache.get(cache_key)
    if cached_data is not None:
        return cached_data['otp_code']
    else:
        otp_code = get_random_string(length=6, allowed_chars="0123456789")
        data_to_cache = {"otp_code": otp_code}
        cache.set(cache_key, data_to_cache, timeout=60)
    return otp_code
