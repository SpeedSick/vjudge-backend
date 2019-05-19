from copy import copy

from authentication.models import Profile
from core.celery import app
from main.models import Assignment, Course, Task, CourseParticipant


def clone_assignment_to_course(assignment_id, course_id):
    assignment = Assignment.objects.get(id=assignment_id)
    cloned_assignment = copy(assignment)
    cloned_assignment.pk = None
    cloned_assignment.id = None
    cloned_assignment.deadline = None
    cloned_assignment.course = Course.objects.get(id=course_id)
    cloned_assignment.save()
    for task in assignment.tasks.all():
        clone_task_to_assignment(task_id=task.id, assignment_id=cloned_assignment.id)
    return cloned_assignment.id


def clone_task_to_assignment(task_id, assignment_id):
    task = Task.objects.get(id=task_id)
    cloned_task = copy(task)
    cloned_task.pk = None
    cloned_task.id = None
    cloned_task.assignment = Assignment.objects.get(id=assignment_id)
    cloned_task.save()
    return cloned_task.id


def get_or_create_course_participant(course_id: int, student_id: int) -> int:
    return CourseParticipant.objects.get_or_create(course_id=course_id, student_id=student_id, is_approved=True).id


def get_profile(user):
    if user.is_anonymous:
        return None
    return Profile.objects.filter(id=user.id).last()
