from main.models import CourseParticipant


def main():
    from authentication.models import User, Profile
    from main.models import Course, Assignment, Task

    user = User.objects.create(
        username='alan',
        first_name='Alan',
        last_name='Amanov',
        password='ZeroTwoHiro1',
        email='alan@alan.alan',
    )

    profile = Profile.objects.create(
        user=user,
        git_username='SpeedSick',
        is_teacher=True,
    )

    student = User.objects.create(
        username='Almat',
        first_name='Almat',
        last_name='Kenen',
        password='ZeroTwoHiro2',
        email='almat@almat.almat',
    )

    student_profile = Profile.objects.create(
        user=student,
        git_username='wtf',
        is_teacher=False,
    )

    course = Course.objects.create(
        name='Programming Technologies',
        teacher=user,
        description='description test test',
    )

    assignment = Assignment.objects.create(
        course=course,
        name='Assignment 1',
        description='description test test',
    )

    course_participant = CourseParticipant.objects.create(
        course=course,
        student=student,
        is_approved=True,
    )
