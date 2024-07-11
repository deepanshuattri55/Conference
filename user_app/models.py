from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

from .consts_ import COUNTRY_CHOICES

class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, affiliation, country, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, affiliation=affiliation, country=country, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, affiliation, country, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, first_name, last_name, affiliation, country, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=50, verbose_name="First Name")
    last_name = models.CharField(max_length=50, verbose_name="Last Name")
    email = models.EmailField(unique=True, verbose_name="Email Address")
    alternate_email = models.EmailField(blank=True, verbose_name="Alternate Email")
    phone = PhoneNumberField(blank=True, null=True, verbose_name="Phone Number")
    affiliation = models.CharField(max_length=100, verbose_name="Affiliation")
    country = models.CharField(max_length=50, choices=COUNTRY_CHOICES, verbose_name="Country")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Created At")

    is_staff = models.BooleanField(default=False, verbose_name="Staff Status")
    is_active = models.BooleanField(default=True, verbose_name="Active Status")

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'affiliation', 'country']

    def __str__(self):
        return self.email