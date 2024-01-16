from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, validate_email
from django.utils.translation import gettext_lazy as _
from django.db import models

from core.mixins import SoftDeleteMixin
from .manager import MyUserManager


class CustomUser(AbstractBaseUser, SoftDeleteMixin, PermissionsMixin):
    """
    handle fields of CustomUser model
    """
    role_choices = [("M", "Manager"), ("S", "Supervisor"), ("O", "Operator"), ("c", "Customer")]
    link_of_connection = [("Ch_Tel", "Chanel Telegram"), ("Ins", "Instagram"), ("Web", "Web Site"), ]
    phonenumber = models.CharField(max_length=50, validators=[RegexValidator(
        regex=r'^(?:\+98|0)?9[0-9]{2}(?:[0-9](?:[ -]?[0-9]{3}){2}|[0-9]{8})$',
        message="Invalid phone number format. Example: +989123456789 or 09123456789", ), ],
                                   verbose_name=_("Phone number"), unique=True)
    email = models.EmailField(max_length=100, verbose_name=_("email address"), validators=[validate_email],
                              unique=True, )
    firstname = models.CharField(max_length=40, verbose_name=_("First name"))
    lastname = models.CharField(max_length=40, verbose_name=_("Last name"))
    how_know_us = models.CharField(choices=link_of_connection, default="False", null=True, max_length=20,
                                   verbose_name=_("how know us"))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("created"))
    updated = models.DateTimeField(auto_now=True, verbose_name=_("updated"))
    is_active = models.BooleanField(default=True, verbose_name=_("is active"))
    is_admin = models.BooleanField(default=True, verbose_name=_("is admin"))

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _("Users")

    objects = MyUserManager()

    USERNAME_FIELD = "phonenumber"
    REQUIRED_FIELDS = ["email", ]

    def __str__(self):
        return f"{self.firstname}_{self.lastname}"

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # user_groups = self.groups.all()
        if self.is_active:
            if self.is_admin:
                return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app """
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        return self.is_admin


class Address(AbstractBaseUser, SoftDeleteMixin, ):
    """ model of users Addresses  """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    city = models.CharField(max_length=40, verbose_name=_("City"))
    address = models.CharField(max_length=40, verbose_name=_("address description"))
    postcode = models.CharField(max_length=40, verbose_name=_("post code"))

    class Meta:
        verbose_name = _('Address')
        verbose_name_plural = _("Addresses")

    def clean(self):
        """validation for postcode length """
        if len(str(self.postcode)) > 10:
            raise ValidationError("Postcode length should be 10 characters or less.")
