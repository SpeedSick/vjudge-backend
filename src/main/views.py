from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .permissions import ApprovedUserAccessPermission, TeacherAccessPermission, StudentAccessPermission
from .serializers import CourseSerializer, CourseParticipantSerializer, AssignmentSerializer, TaskSerializer
from .models import Course, Assignment, Task, CourseParticipant


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
            queryset = queryset.filter(course=data['course'])
        if 'student' in data and data['student'] == self.request.user.id:
            queryset = queryset.filter(student=data['student'])
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
        if self.action in ('update', 'partial_update', 'destroy'):
            queryset = queryset.filter(course__teacher=self.request.user)
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
        if self.action in ('update', 'partial_update', 'destroy'):
            queryset = queryset.filter(assignment__course__teacher=self.request.user)
        return queryset
