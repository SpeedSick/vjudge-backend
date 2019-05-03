from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from authentication.models import Profile
from .permissions import ApprovedUserAccessPermission, TeacherAccessPermission, StudentAccessPermission, \
    CustomTokenPermission
from .serializers import CourseSerializer, CourseParticipantSerializer, AssignmentSerializer, TaskSerializer, \
    ResultSerializer
from .models import Course, Assignment, Task, CourseParticipant, Result


class CourseViewSet(ModelViewSet):
    def get_permissions(self):
        permission_classes = []
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            permission_classes = [
                IsAuthenticated,
                ApprovedUserAccessPermission,
                TeacherAccessPermission,
            ]
        return [permission() for permission in permission_classes]

    serializer_class = CourseSerializer

    def get_queryset(self):
        queryset = Course.objects.all()
        data = self.request.query_params

        if self.action in ('update', 'partial_update', 'destroy'):
            queryset = queryset.filter(teacher=self.request.user)

        if 'teacher' in data:
            queryset = queryset.filter(teacher=data['teacher'])
        print(queryset)
        if 'student' in data:
            queryset = queryset.filter(participants__student=self.request.user)
        print(queryset)
        print('wtf')

        return queryset.order_by('-modified')


class CourseParticipantViewSet(ModelViewSet):
    def get_permissions(self):
        permission_classes = []
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            permission_classes = [
                IsAuthenticated,
                ApprovedUserAccessPermission,
                StudentAccessPermission,
            ]
        return [permission() for permission in permission_classes]

    serializer_class = CourseParticipantSerializer

    def get_queryset(self):

        queryset = CourseParticipant.objects.all()
        data = self.request.query_params

        if 'course' in data:
            course = Course.objects.filter(pk=data['course']).last()

            if course.teacher == self.request.user:
                queryset = queryset.filter(course=course)
            else:
                queryset = queryset.none()

        if 'student' in data:
            queryset = queryset.filter(student=self.request.user)
        elif 'teacher' in data:
            queryset = queryset.filter(course__teacher=self.request.user)
        else:
            queryset = queryset.none()

        return queryset.order_by('-joined')


class AssignmentViewSet(ModelViewSet):

    def get_permissions(self):
        permission_classes = []
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            permission_classes = [
                IsAuthenticated,
                ApprovedUserAccessPermission,
                TeacherAccessPermission,
            ]
        return [permission() for permission in permission_classes]

    serializer_class = AssignmentSerializer

    def get_queryset(self):
        queryset = Assignment.objects.all()
        data = self.request.query_params

        if self.action in ('update', 'partial_update', 'destroy'):
            queryset = queryset.filter(course__teacher=self.request.user)

        if 'course' in data:
            course = Course.objects.filter(pk=data['course']).last()
            if course.teacher == self.request.user:
                queryset = queryset.filter(course=course)
            else:
                queryset = queryset.none()

        elif 'student' in data:
            queryset = queryset.filter(student=self.request.user.id)
        else:
            queryset = queryset.none()

        return queryset


class TaskViewSet(ModelViewSet):

    def get_permissions(self):
        permission_classes = []
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            permission_classes = [
                IsAuthenticated,
                ApprovedUserAccessPermission,
                TeacherAccessPermission,
            ]
        return [permission() for permission in permission_classes]

    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = Task.objects.all()
        data = self.request.query_params
        if self.action in ('update', 'partial_update', 'destroy'):
            queryset = queryset.filter(assignment__course__teacher=self.request.user)
        if 'assignment' in data:
            profile = Profile.objects.filter(user=self.request.user).last()
            assignment = Assignment.objects.filter(pk=data['assignment']).last()
            if profile.is_teacher:
                queryset = queryset.filter(assignment=assignment)
            else:
                queryset = queryset.filter(assignment=assignment,
                                           assignment__course__participants__student=self.request.user)
        else:
            queryset = queryset.none()
        return queryset


class ResultCreateAPIView(generics.CreateAPIView):
    serializer_class = ResultSerializer
    queryset = Result.objects.all()
    permission_classes = (CustomTokenPermission,)
