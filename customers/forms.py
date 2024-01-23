from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
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
    phone = forms.CharField(max_length=100, label='Please enter your Phone number ',
                            widget=forms.TextInput(attrs={"class": "form-control",
                                                          "placeholder": "Phone number",
                                                          "style": "background: transparent !important;", }))


# def clean_email(self):
#     phone = self.cleaned_data['phone']
#     user = CustomUser.objects.filter(phonenumber=phone).exists()
#     if user:
#         raise ValidationError('this Phone number already exist')
#     return phone


class VerifyCodeFrom(forms.Form):
    code = forms.CharField(max_length=20, label='Please enter the verification code',
                           widget=forms.TextInput(attrs={"class": "form-control",
                                                         "placeholder": "verification code",
                                                         "style": "background: transparent !important;", }))


class UserLoginForm(forms.Form):
    pass
