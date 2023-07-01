import uuid

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from user_manager.manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(
        "User ID", primary_key=True, default=uuid.uuid4, editable=False
    )
    name = models.CharField("User Name", max_length=255, blank=True, null=True)
    email = models.EmailField(
        "User Email", default=None, blank=True, null=True, unique=True
    )
    phone = models.CharField(
        "User Phone No.",
        max_length=15,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex="^09[0-9]*$",
                message="Phone number must start with 09 and must only contain numbers.",
                code="Phone number invalid",
            )
        ],
    )
    is_staff = models.BooleanField("Staff Status", default=False)
    is_active = models.BooleanField("Active Status", default=False)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token_for_user(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# Create your models here.
