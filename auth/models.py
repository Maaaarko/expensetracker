from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from rest_framework_simplejwt.tokens import RefreshToken


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if email is None:
            raise ValueError("No email provided.")

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None):
        if password is None:
            raise TypeError("No password provided.")

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

AUTH_PROVIDERS = {
        "email": "email",
        "google":"google",
    }

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    provider = models.CharField(max_length=255, blank=False, null=False, default=AUTH_PROVIDERS.get("email"))

    CURRENCY_CHOICES = [
        ("USD", "$"),
        ("GBP", "£"),
        ("EUR", "€")
    ]

    currency = models.CharField(max_length=3, default="USD", choices=CURRENCY_CHOICES)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    
    objects = UserManager()

    def __str__(self):
        return self.username
    
    def tokens(self):
        refresh_token = RefreshToken.for_user(self)
        return {
            "refresh_token": str(refresh_token),
            "access_token": str(refresh_token.access_token)
        }


