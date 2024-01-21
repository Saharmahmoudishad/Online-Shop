from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.messages.views import SuccessMessageMixin
from django.core.cache import cache
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.crypto import get_random_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View
from django.views.generic import TemplateView, CreateView, FormView
from django.contrib.auth.views import PasswordResetView
from utils import send_registration_email, send_otp_code_by_phone
from .forms import VerifyCodeFrom, RequestRegisterByEmailForm, \
    RequestRegistrationByPhoneFrom, UserCreationForm
from .models import CustomUser

user = get_user_model()


# Create your views here.
class RequestRegisterView(FormView):
    model = CustomUser
    template_name = 'customers/registeration_by_email.html'
    success_url = reverse_lazy('core:home')
    form_class = RequestRegisterByEmailForm
    token_generator = default_token_generator
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

    def form_valid(self, form):
        email = form.cleaned_data['email']
        self.request.session['user_registration_info'] = {'email': email}
        protocol = 'http' if not self.request.is_secure() else 'https'
        domain = self.request.META['HTTP_HOST']

        send_registration_email(email, self.uidb64, self.token_generator, protocol, domain)
        messages.success(self.request, "The authentication confirmation link has been sent to your email", "success")
        return super().form_valid(form)


class CompleteRegisterByEmailView(SuccessMessageMixin, CreateView):
    model = CustomUser
    template_name = 'customers/complete_register_by_email_form.html'
    success_url = reverse_lazy('core:home')
    form_class = UserCreationForm
    success_message = 'Account created successfully. You can now log in.'

    def form_valid(self, form):
        response = super().form_valid(form)
        user_email = self.request.session.get('user_registration_info', {}).get('email')
        if user_email:
            self.object.email = user_email
            self.object.save()
        return response


class RequestRegisterByPhoneView(View):
    form_class = RequestRegistrationByPhoneFrom
    template_name = 'customers/register_by_phone.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('core:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            otp_code = self.generate_and_store_otp(phone)
            send_otp_code_by_phone(phone, otp_code)
            request.session['user_registration_info'] = {'phone': phone}
            messages.success(request, "send registeration code to your Phone Number", "success")
            return redirect('customers:verify_registeration_code')
        return render(request, self.template_name, {'form': form})

    @staticmethod
    def generate_and_store_otp(email):
        cache_key = email
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return cached_data['otp_code']
        else:
            otp_code = get_random_string(length=6, allowed_chars="0123456789")
            data_to_cache = {"otp_code": otp_code}
            cache.set(cache_key, data_to_cache, timeout=60)
        return otp_code


class CompleteRegisterVerifyCodeView(View):
    form_class = VerifyCodeFrom
    template_name = 'customers/verify_code.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('core:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class
        return render(request, 'customers/verify_code.html', {'form': form})

    def post(self, request):
        user_session = request.session['user_registration_info']
        code_instance = cache.get(user_session['phone'])
        # code_instance = cache.get(email=user_session['email'])
        form = self.form_class(request.POST)
        if form.is_valid():
            otp_code = form.cleaned_data['code']
            if code_instance['otp_code'] == otp_code:
                CustomUser.objects.create_user(phone=user_session['phone'])
                messages.success(request, 'you registered', 'success')
                return redirect('core:home')
            else:
                messages.error(request, 'this code is wrong', 'danger')


class CustomerloginCodeView(View):
    def get(self, request):
        pass

    def post(self, request):
        pass


class CustomerlogoutCodeView(View):
    def get(self, request):
        pass
