from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

from django.contrib.auth import get_user_model
from django.utils import timezone


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(email, password)

        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=60)

    last_name = models.CharField(max_length=60)
    username = models.CharField(max_length=60, unique=True)

    referral_id = models.CharField(max_length=10, unique=True)
    is_verified = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

User = get_user_model()


class Referral(models.Model):
    referred_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='referral')
    referrer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='referrals')
    created_at = models.DateTimeField(default=timezone.now)
