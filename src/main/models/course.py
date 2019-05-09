from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q

from .course_participant import CourseParticipant


class Course(models.Model):
    teacher = models.ForeignKey(User, related_name='teacher_courses', on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=2047)
    image = models.ImageField(null=True)
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)

    @property
    def participants(self):
        return [course_participant.student.id for course_participant in
                CourseParticipant.objects.filter(Q(course=self) & Q(is_approved=True))]
