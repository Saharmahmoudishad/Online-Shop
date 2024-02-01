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
from utils import generate_and_store_otp, send_otpcode_email, send_registration_email, kave_negar_token_send
from django.contrib.auth import views as auth_view
from .forms import VerifyCodeFrom, RequestRegisterByEmailForm, \
    RequestRegistrationByPhoneFrom, UserCreationForm, CustomAuthenticationForm
from .models import CustomUser

user = get_user_model()


class RequestRegisterView(FormView):
    """handle Request of user for register
    if user sign in for first time, this class send email by link for register
    if user registered before, this class send email by code for login
    """
    model = CustomUser
    template_name = 'customers/registeration_by_email.html'
    success_url = reverse_lazy('core:home')
    form_class = RequestRegisterByEmailForm
    token_generator = default_token_generator
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('core:home')
        return super().dispatch(request, *args, **kwargs)

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
    """complete registeration by post register form"""
    model = CustomUser
    template_name = 'customers/complete_register_by_email_form.html'
    success_url = reverse_lazy('core:home')
    form_class = UserCreationForm
    success_message = 'Account created successfully. You can now log in.'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('core:home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        user_email = self.request.session.get('user_registration_info', {}).get('email')
        if user_email:
            self.object.email = user_email
            self.object.save()
        return response


class LoginVerifyCodeView(View):
    """sign in user by email who is registered before by sending code"""
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
    """handle Request of user for register by phonenumber and otp code"""
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
            phone = form.cleaned_data['phonenumber']
            otp_code = generate_and_store_otp(phone)
            print("1" * 50, otp_code)
            # kave_negar_token_send(phone, otp_code)
            request.session['user_registration_info'] = {'phone': phone}
            messages.success(request, "send registeration code to your Phone Number", "success")
            return redirect('customers:verify_registeration_code')
        return render(request, self.template_name, {'form': form})


class CompleteRegisterVerifyCodeView(View):
    """complete sign in user by phone_number and verification code """
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
        code_instance = cache.get(user_session)['otp_code']
        form = self.form_class(request.POST)
        if form.is_valid():
            otp_code = form.cleaned_data['code']
            if code_instance == otp_code:
                requester = user.objects.filter(phonenumber=user_session).first()
                if requester:
                    login(request, requester, backend='django.contrib.auth.backends.ModelBackend')
                    messages.success(request, 'you login successfully', 'success')
                    return redirect('core:home')
                else:
                    CustomUser.objects.create_user(phone=user_session, password="")
                    messages.success(request, 'you registered', 'success')
                    return redirect('core:home')
            else:
                messages.error(request, 'this code is wrong', 'danger')
                return redirect('customers:verify_registeration_code')
        else:
            messages.error(request, 'Invalid form submission', 'danger')
            return render(request, self.template_name, {'form': form})


class UserLoginByPassView(auth_view.LoginView):
    """complete sign in user by password """
    template_name = 'customers/login_bypassword.html'
    success_url = reverse_lazy('core:home')
    form_class = CustomAuthenticationForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('core:home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        identifier_value = self.kwargs['identifier']
        print("1"*50,identifier_value)
        super().form_valid(form)
        username_from_session = self.request.session.get('user_registration_info', {}).get(identifier_value)
        print("1" * 50, username_from_session)
        if username_from_session:
            form.cleaned_data['username'] = username_from_session
            if identifier_value =='email':
               user_login = authenticate(self.request, username=username_from_session, password=form.cleaned_data['password'])
            else:
                user_login = authenticate(self.request, username=username_from_session, password=form.cleaned_data['password'])
                print("2" * 50, user_login)
            if user_login is not None:
                login(self.request, user_login)
                return redirect(reverse('core:home'))
        return redirect(reverse('customers:user_login_by_pass', kwargs={'identifier': identifier_value}))

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid login credentials. Please try again.')
        return redirect(reverse('customers:user_login_by_pass', kwargs={'identifier':self.kwargs['identifier']}))


class UserLogoutView(auth_view.LogoutView):
    """handle logout of users"""

    def get_success_url(self):
        return self.request.GET.get('next', reverse_lazy('core:home'))


class UserPasswordResetView(auth_view.PasswordResetView):
    template_name = 'customers/resetpassword/password_resetform.html'
    success_url = reverse_lazy('customers:password_reset_done')
    email_template_name = "customers/resetpassword/password_reset_email.html"


class UserPasswordResetDoneView(auth_view.PasswordResetDoneView):
    template_name = 'customers/resetpassword/password_reset_done.html'


class UserPasswordResetConfirmView(auth_view.PasswordResetConfirmView):
    template_name = 'customers/resetpassword/password_reset_confirm.html'
    success_url = reverse_lazy('customers:password_reset_completed')


class UserPasswordResetCompleteView(auth_view.PasswordResetCompleteView):
    template_name = 'customers/resetpassword/password_reset_complete.html'
