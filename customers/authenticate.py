from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from customers.models import CustomUser


class EmailBackend(ModelBackend) :
    user = get_user_model()

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = self.user.objects.get(email=username)
            if user.check_password(password):
                return user
        except self.user.DoesNotExist:
            return None

