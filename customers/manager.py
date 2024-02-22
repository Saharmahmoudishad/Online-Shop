from django.contrib.auth.base_user import BaseUserManager


class MyUserManager(BaseUserManager):
    """
     Custom manager for the CustomUser model.
     """
    def get_queryset(self):
        """
        Returns a queryset that filters out users marked as deleted.
        """
        return super().get_queryset().filter(is_deleted=False)

    def create_user(self, phonenumber, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given phonenumber,email and password.
        """
        if not (phonenumber or email):
            raise ValueError("Users must have an phone number")
        email = self.normalize_email(email)
        user = self.model(phonenumber=phonenumber, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phonenumber, email=None, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given phonenumber, nickname, email and password.
        """
        user = self.create_user(phonenumber, email, password=password, )
        user.is_admin = True
        user.save(using=self._db)
        return user


