from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver

from authentication.models import User


class Assignment(models.Model):
    course = models.ForeignKey('Course', related_name='assignments', on_delete=models.CASCADE)
    folder_name = models.CharField(default='', max_length=255)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=2047)
    deadline = models.DateTimeField(null=True)
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)
    git_fork_link = models.CharField(max_length=255)

    @receiver(post_save, sender='main.Assignment')
    def create_news_for_assignments(sender, instance=None, created=False, **kwargs):
        if created:
            for participant in instance.course.participants.all():
                News.objects.create(user=participant.student, course=instance.course,
                                    message=News.STATUS_NEW_ASSIGNMENT)


class CourseParticipant(models.Model):
    is_approved = models.BooleanField(default=False)
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='participants')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='participations')
    joined = models.DateField(auto_now_add=True)
    git_repository_name = models.CharField(max_length=255)

    @receiver(post_save, sender='main.CourseParticipant')
    def create_news_for_assignments(sender, instance=None, created=False, **kwargs):
        if created:
            News.objects.get_or_create(user=instance.course.teacher, course=instance.course,
                                       message=News.STATUS_APPROVE_REQUIRED, seen=False)

    class Meta:
        unique_together = (('student', 'course'),)


class Course(models.Model):
    teacher = models.ForeignKey(User, related_name='teacher_courses', on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=2047)
    image = models.ImageField(null=True)
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)

    @property
    def students(self):
        return [course_participant.student.id for course_participant in
                CourseParticipant.objects.filter(Q(course=self) & Q(is_approved=True))]

    @property
    def notifications(self):
        return self.news.filter(seen=False)


class News(models.Model):
    STATUS_APPROVE_REQUIRED = "You have many requests for this course, please follow the link to view them"
    STATUS_SUBMISSIONS_GRADED = "Your submission has been graded, go over the link to see the submission results"
    STATUS_NEW_ASSIGNMENT = "You have new assignment to do"
    STATUSES = (
        (STATUS_APPROVE_REQUIRED, STATUS_APPROVE_REQUIRED),
        (STATUS_SUBMISSIONS_GRADED, STATUS_SUBMISSIONS_GRADED),
        (STATUS_NEW_ASSIGNMENT, STATUS_NEW_ASSIGNMENT),
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='news')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255, choices=STATUSES)
    seen = models.BooleanField(default=False)


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
