from django.db import models
from authentication.models import User


class CourseParticipant(models.Model):
    is_approved = models.BooleanField(default=False)
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='participants')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='participations')
    joined = models.DateField(auto_now_add=True)


class Course(models.Model):
    teacher = models.ForeignKey(User, related_name='teacher_courses', on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=2047)
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)


class Assignment(models.Model):
    course = models.ForeignKey(Course, related_name='assignments', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=2047)
    deadline = models.DateTimeField(null=True)
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)


class Task(models.Model):
    assignment = models.ForeignKey(Assignment, related_name='tasks', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1023)
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)


class Test(models.Model):
    task = models.ForeignKey(Task, related_name='tests', on_delete=models.CASCADE)
    test_file = models.FileField()


class Submission(models.Model):
    task = models.ForeignKey(Task, related_name='submissions', on_delete=models.DO_NOTHING)
    course_participant = models.ForeignKey(CourseParticipant, related_name='submissions', on_delete=models.DO_NOTHING)
