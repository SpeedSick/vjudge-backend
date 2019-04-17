from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Profile(User):
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    git_username = models.CharField(max_length=255)
