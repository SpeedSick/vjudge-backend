from django.db import models
from .course import Course


class Assignment(models.Model):
    course = models.ForeignKey(Course, related_name='assignments', on_delete=models.CASCADE)
    folder_name = models.CharField(default='', max_length=255)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=2047)
    deadline = models.DateTimeField(null=True)
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)
