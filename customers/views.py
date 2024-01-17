from django.contrib import messages
from django.core.cache import cache
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string
from django.views import View
from django.views.generic import TemplateView

from utils import send_registration_email
from .forms import UserRegistrationFrom, VerifyCodeFrom
from .models import CustomUser


# Create your views here.
class CustomerRegisterView(View):
    form_class = UserRegistrationFrom
    template_name = 'customers/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class
        return render(request, 'customers/register.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            otp_code = self.generate_and_store_otp(email)
            send_registration_email(email, otp_code)
            request.session['user_registration_info'] = {'email': email}
            messages.success(request, "send registeration code to your email", "success")
            return redirect('customer:verify_registeration_code')
        return render(request, self.template_name, {'form': form})

    @staticmethod
    def generate_and_store_otp(email):
        otp_code = get_random_string(length=6, allowed_chars="0123456789")
        cache_key = "email"
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return cached_data
        else:
            data_to_cache = {"otp_code": otp_code}
            cache.set(cache_key, data_to_cache, timeout=60)
        return otp_code


class CustomerRegisterVerifyCodeView(View):
    form_class = VerifyCodeFrom
    template_name = 'customers/verify_code.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class
        return render(request, 'customers/verify_code.html', {'form': form})

    def post(self, request):
        user_session = request.session['user_registration_info']
        code_instance = cache.get(email=user_session['email'])
        form = self.form_class(request.POST)
        if form.is_valid():
            otp_code = form.cleaned_data['code']
        if code_instance['otp_code'] == otp_code:
            CustomUser.objects.create_user(email=user_session['email'])


class CustomerloginCodeView(View):
    def get(self, request):
        pass

    def post(self, request):
        pass


class CustomerlogoutCodeView(View):
    def get(self, request):
        pass
