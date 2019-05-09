from django.contrib.auth.models import User
from django.db import models


class CourseParticipant(models.Model):
    is_approved = models.BooleanField(default=False)
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='participants')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='participations')
    joined = models.DateField(auto_now_add=True)
    git_repository_name = models.CharField(max_length=255)
