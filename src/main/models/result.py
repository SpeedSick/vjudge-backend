from django.db import models

from .submission import Submission


class Result(models.Model):
    submission = models.ForeignKey(Submission, related_name='results', on_delete=models.CASCADE)
    score = models.DecimalField(decimal_places=2, default=0, max_digits=5)
