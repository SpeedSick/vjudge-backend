from django.db import models

from .course_participant import CourseParticipant
from .task import Task


class Submission(models.Model):
    task = models.ForeignKey(Task, related_name='submissions', on_delete=models.DO_NOTHING)
    course_participant = models.ForeignKey(CourseParticipant, related_name='submissions', on_delete=models.DO_NOTHING)
