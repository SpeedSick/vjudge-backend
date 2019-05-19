from django.contrib.auth.models import User
from django.db import models

from authentication.utils import gen_token


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True)
    is_teacher = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=True)
    git_username = models.CharField(max_length=255)


class PasswordResetToken(models.Model):
    token = models.CharField(max_length=10, blank=False, default=gen_token)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
