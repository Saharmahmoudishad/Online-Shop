from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from customers.models import CustomUser


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = '__all__'

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


class UserRegistrationFrom(forms.Form):
    email_or_phone = forms.CharField(max_length=100, label='Please enter your Phone number or Email',
                                     widget=forms.TextInput(attrs={"class": "form-control",
                                                                   "placeholder": "Phone number or Email",
                                                                   "style": "background: transparent !important;", }))


class VerifyCodeFrom(forms.Form):
    code = forms.CharField(max_length=20, label='Please enter the verification code sent to the email',
                           widget=forms.TextInput(attrs={"class": "form-control",
                                                         "placeholder": "verification code",
                                                         "style": "background: transparent !important;", }))


class UserLoginForm(forms.Form):
    pass
