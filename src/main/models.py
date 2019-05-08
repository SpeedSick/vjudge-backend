from django.db import models
from authentication.models import User


class CourseParticipant(models.Model):
    is_approved = models.BooleanField(default=True)
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='participants')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='participations')
    joined = models.DateField(auto_now_add=True)
    git_repository_name  = models.CharField(max_length=255)

class Course(models.Model):
    teacher = models.ForeignKey(User, related_name='teacher_courses', on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=2047)
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)


class Assignment(models.Model):
    course = models.ForeignKey(Course, related_name='assignments', on_delete=models.CASCADE)
    folder_name = models.CharField(default='', max_length=255)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=2047)
    deadline = models.DateTimeField(null=True)
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)


class Task(models.Model):
    assignment = models.ForeignKey(Assignment, related_name='tasks', on_delete=models.CASCADE)
    folder_name = models.CharField(default='', max_length=255)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1023)
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)
    testfile = models.FileField(null=True)


class Submission(models.Model):
    task = models.ForeignKey(Task, related_name='submissions', on_delete=models.DO_NOTHING)
    course_participant = models.ForeignKey(CourseParticipant, related_name='submissions', on_delete=models.DO_NOTHING)


class Result(models.Model):
    submission = models.ForeignKey(Submission, related_name='results', on_delete=models.CASCADE)
    score = models.DecimalField(decimal_places=2, default=0, max_digits=5)
