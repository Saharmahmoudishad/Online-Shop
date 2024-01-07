from django.contrib.auth.base_user import BaseUserManager


# Create your models here.
class MyUserManager(BaseUserManager):
    def create_user(self, phonenumber, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given phonenumber,email and password.
        """
        if not phonenumber:
            raise ValueError("Users must have an phonenumber")
        email = self.normalize_email(email)
        user = self.model(phonenumber=phonenumber, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
