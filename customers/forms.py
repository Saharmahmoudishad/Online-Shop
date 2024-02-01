from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AuthenticationForm
from django.core.exceptions import ValidationError

from customers.models import CustomUser


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('phonenumber', "firstname", "lastname", "how_know_us",)

    def clean(self):
        datas = super().clean()
        p1 = datas.get("password1")
        p2 = datas.get("password2")
        if p1 and p2 and p1 != p2:
            self.add_error('password2', "your confirm password and password does not match")

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admins
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField(
        help_text="you cant change password Using <a href=\"../password/\">this form</a>")

    class Meta:
        model = CustomUser
        fields = ["phonenumber", "email",
                  "password", "firstname", "lastname", "how_know_us",
                  "is_active", "is_admin", "is_deleted"]


class RequestRegisterByEmailForm(forms.Form):
    email = forms.CharField(max_length=100, label='Please enter your Email',
                            widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Email",
                                                          "style": "background: transparent !important; border: 1px solid darkorange;", }))

    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     if CustomUser.objects.filter(email=email).exists():
    #         raise ValidationError("This email is already registered.Please sign in", code='email_exists')
    #     return email


class RequestRegistrationByPhoneFrom(forms.Form):
    phonenumber = forms.CharField(max_length=100, label='Please enter your Phone number ',
                            widget=forms.TextInput(attrs={"class": "form-control",
                                                          "placeholder": "Phone number",
                                                          "style": "background: transparent !important;", }))




class VerifyCodeFrom(forms.Form):
    code = forms.CharField(max_length=20, label='Please enter the verification code', error_messages={
        'required': 'Please enter the verification code.',
        'invalid': 'Invalid code format. Please enter a valid code.', },
                           widget=forms.TextInput(attrs={"class": "form-control",
                                                         "placeholder": "verification code",
                                                         "style": "background: transparent !important;", }))


class CustomAuthenticationForm(AuthenticationForm):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    phonenumber/password logins.
    """
    username = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control", "autocomplete": "off",
               'placeholder': 'Enter your phone number or email address',
               "style": "background: transparent !important;"}),
        help_text="Please enter a valid phone number of email address.",
        label='phone number or Email Address')
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={"class": "form-control", "autocomplete": "off", 'placeholder': 'Enter your password',
               "style": "background: transparent !important;"}), help_text="forgot your" "password", )

