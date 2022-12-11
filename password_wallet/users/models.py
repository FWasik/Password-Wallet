from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


class CustomUserManager(BaseUserManager):
    def create_user(self, login: str, password: str, **extra_fields):
        if not login:
            raise ValueError(_("Login must be set"))

        user = self.model(login=login, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, login: str, password: str, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(login, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    login = models.CharField(max_length=512, unique=True)
    is_password_checked = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    unsuccessful_time_login = models.DateTimeField(null=True, default=None)

    USERNAME_FIELD = "login"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.login




