from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager

# Create your models here.


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    api_key = models.CharField(max_length=100, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email


class Domain(models.Model):
    domain = models.CharField(max_length=200) #origin
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    permission = models.CharField(max_length=200, blank=True, null=True) #permissions
    domain_key = models.CharField(max_length=100) #aipkey
    ekycxml_endpoint = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.user.email + " - " + self.domain
