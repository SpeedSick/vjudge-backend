from django.db import models

from .assignment import Assignment


class Task(models.Model):
    assignment = models.ForeignKey(Assignment, related_name='tasks', on_delete=models.CASCADE)
    folder_name = models.CharField(default='', max_length=255)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1023)
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)
    testfile = models.FileField(null=True)
