from django.contrib import messages
from django.contrib.auth import get_user_model, login, authenticate
from django.contrib.auth.tokens import default_token_generator
from django.contrib.messages.views import SuccessMessageMixin
from django.core.cache import cache
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views import View
from django.views.generic import CreateView, FormView
from django.contrib.auth import views as auth_view
from utils import send_registration_email, send_otp_code_by_phone, generate_and_store_otp, send_otpcode_email
from .forms import VerifyCodeFrom, RequestRegisterByEmailForm, \
    RequestRegistrationByPhoneFrom, UserCreationForm, CustomAuthenticationForm
from .models import CustomUser

user = get_user_model()


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
        requester = user.objects.filter(email=email).exists()
        if requester:
            otp_code = generate_and_store_otp(email)
            send_otpcode_email(email, otp_code, )
            return redirect('customers:verify_login_code')
        else:
            protocol = 'http' if not self.request.is_secure() else 'https'
            domain = self.request.META['HTTP_HOST']
            send_registration_email(email, self.uidb64, self.token_generator, protocol, domain)
            messages.success(self.request, "The authentication confirmation link has been sent to your email",
                             "success")
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


class LoginVerifyCodeView(View):
    form_class = VerifyCodeFrom
    template_name = 'customers/verify_code_toemail.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('core:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        user_session = self.request.session.get('user_registration_info', {}).get('email')
        code_instance = cache.get(user_session)
        form = self.form_class(request.POST)
        try:
            if form.is_valid():
                otp_code = form.cleaned_data['code']
                if otp_code == code_instance['otp_code']:
                    requester = user.objects.filter(email=user_session).first()
                    login(request, requester, backend='django.contrib.auth.backends.ModelBackend')
                    return redirect('core:home')
                else:
                    return render(request, self.template_name, {'form': form})
        except:
            messages.error(request, 'Code is expired', 'danger')
            return redirect('customers:request_register_by_email')


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
            otp_code = generate_and_store_otp(phone)
            print("3" * 60, "saraaaa")
            send_otp_code_by_phone(phone, otp_code)
            print("4 " * 60, "saraaaa")
            request.session['user_registration_info'] = {'phone': phone}
            messages.success(request, "send registeration code to your Phone Number", "success")
            return redirect('customers:verify_registeration_code')
        return render(request, self.template_name, {'form': form})


class CompleteRegisterVerifyCodeView(View):
    form_class = VerifyCodeFrom
    template_name = 'customers/verify_code.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('core:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        user_session = self.request.session.get('user_registration_info', {}).get('phone')
        code_instance = cache.get(user_session)
        # code_instance = cache.get(email=user_session['email'])
        form = self.form_class(request.POST)
        if form.is_valid():
            print("7" * 60, "saraaaa")
            otp_code = form.cleaned_data['code']
            if code_instance['otp_code'] == otp_code:
                requester = user.objects.filter(phonenumber=user_session).exists()
                if requester:
                    messages.success(request, 'you login successfully', 'success')
                else:
                    CustomUser.objects.create_user(phone=user_session['phone'], password="")
                    messages.success(request, 'you registered', 'success')
                    return redirect('core:home')
            else:
                messages.error(request, 'this code is wrong', 'danger')
                return redirect('accounts:verify_code')


class UserLoginByPassView(auth_view.LoginView):
    template_name = 'customers/login_bypassword.html'
    success_url = reverse_lazy('core:home')
    form_class = CustomAuthenticationForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('core:home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        email_from_session = self.request.session.get('user_registration_info', {}).get('email')
        if email_from_session:
            form.cleaned_data['username'] = email_from_session
            user = authenticate(self.request, email=email_from_session, password=form.cleaned_data['password'])
            if user is not None:
                login(self.request, user)
                return redirect(reverse('core:home'))
        return redirect(reverse('customers:user_login_by_pass'))

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid login credentials. Please try again.')
        return redirect(reverse('customers:user_login_by_pass'))


class UserLogoutView(auth_view.LogoutView):
    class UserLogoutView(auth_view.LogoutView):
        def get_success_url(self):
            return self.request.GET.get('next', reverse_lazy('core:home'))
