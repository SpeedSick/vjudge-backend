from django.db import models
from authentication.models import Profile


# Create your models here.


class CourseParticipant(models.Model):
    is_approved = models.BooleanField(default=False)
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='participants')
    student = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='participations')


class Course(models.Model):
    teacher = models.ForeignKey(Profile, related_name='teacher_courses', on_delete=models.DO_NOTHING)
    assistants = models.ManyToManyField(Profile, related_name='assistant_courses')


class Assignment(models.Model):
    course = models.ForeignKey(Course, related_name='assignments', on_delete=models.CASCADE)
    deadline = models.DateTimeField()


class Task(models.Model):
    assignment = models.ForeignKey(Assignment, related_name='tasks', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1023)


class Test(models.Model):
    task = models.ForeignKey(Task, related_name='tests', on_delete=models.CASCADE)
    test_file = models.FileField()


class Submission(models.Model):
    task = models.ForeignKey(Task, related_name='submissions', on_delete=models.DO_NOTHING)
    course_participant = models.ForeignKey(CourseParticipant, related_name='submissions', on_delete=models.DO_NOTHING)
