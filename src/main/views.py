from rest_framework import generics, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from authentication.models import Profile, User
from grader.tasks import check_submissions, grade
from main.models import News, Submission
from main.serializers.course_participant import CourseParticipantApproveSerializer, CourseParticipantUpdateSerializer
from main.serializers.submission import SubmissionSerializer, SubmissionRetrieveSerializer, SubmissionPostSerializer
from main.utils import get_profile
from .permissions import ApprovedUserAccessPermission, TeacherAccessPermission, StudentAccessPermission, \
    CustomTokenPermission
from .serializers import CoursePostSerializer, CourseGetSerializer, CourseParticipantSerializer, AssignmentSerializer, \
    TaskSerializer, \
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
        if self.action in ('register',):
            permission_classes = {
                IsAuthenticated,
                ApprovedUserAccessPermission,
                StudentAccessPermission
            }
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        serializer_class = CourseGetSerializer
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            serializer_class = CoursePostSerializer
        elif self.action == 'register':
            serializer_class = CourseParticipantUpdateSerializer
        return serializer_class

    def get_queryset(self):
        queryset = Course.objects.all()
        data = self.request.query_params
        if self.action in ('update', 'partial_update', 'destroy'):
            queryset = queryset.filter(teacher=self.request.user)
        if 'teacher' in data:
            queryset = queryset.filter(teacher=data['teacher'])
        if 'student' in data:
            queryset = queryset.filter(participants__student=self.request.user)
        return queryset.order_by('-modified')

    @action(detail=True, methods=['post'])
    def register(self, request, pk=None):
        data = {
            'student': request.user.id,
            'course': pk,
            'is_approved': False,
        }
        if request.data.get('git_repository_name'):
            data['git_repository_name'] = request.data['git_repository_name']
        serialized = CourseParticipantSerializer(data=data)
        if serialized.is_valid(raise_exception=True):
            CourseParticipant.objects.create(**serialized.validated_data)
            return Response(data=serialized.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def participation(self, request, pk=None):
        if request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        participation = CourseParticipant.objects.filter(student_id=self.request.user.id, course=pk,
                                                         is_approved=True).last()
        if participation is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        data = {
            'student': request.user.id,
            'course': pk,
            'is_approved': True,
        }
        serialized = CourseParticipantSerializer(data=data)
        if serialized.is_valid(raise_exception=True):
            return Response(status=status.HTTP_200_OK, data=serialized.data)

    def finalize_response(self, request, response, *args, **kwargs):
        if self.action in ('retrieve',):
            user = request.user
            if not user.is_anonymous:
                news = News.objects.filter(user=user, course=self.get_object(), seen=False)
                for seen_news in news:
                    seen_news.seen = True
                    seen_news.save()
        return super(CourseViewSet, self).finalize_response(request, response, *args, **kwargs)


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
        if self.action in ('update', 'partial_update', 'destroy',):
            queryset = queryset.filter(course__teacher=self.request.user.id)
        elif self.action in ('retrieve', 'list',):
            queryset = queryset.filter(course__teacher=self.request.user.id) | queryset.filter(
                course__participants__student=self.request.user.id)
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
        else:
            permission_classes = [
                IsAuthenticated,
                ApprovedUserAccessPermission,
            ]
        return [permission() for permission in permission_classes]

    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = Task.objects.all()
        data = self.request.query_params
        if self.action in ('update', 'partial_update', 'destroy'):
            queryset = queryset.filter(assignment__course__teacher=self.request.user)
        if 'assignment' in data:
            profile = get_profile(self.request.user)
            if profile is None:
                return Task.objects.none()
            assignment = Assignment.objects.filter(pk=data['assignment']).last()
            if profile.is_teacher:
                queryset = queryset.filter(assignment=assignment)
            else:
                queryset = queryset.filter(assignment=assignment,
                                           assignment__course__participants__student=self.request.user)
        else:
            queryset = queryset.filter(assignment__course__teacher=self.request.user) | queryset.filter(
                assignment__course__participants__student=self.request.user)
        return queryset


class ResultCreateAPIView(generics.CreateAPIView):
    serializer_class = ResultSerializer
    queryset = Result.objects.all()
    permission_classes = (CustomTokenPermission,)


class ApproveCourseParticipant(APIView):
    permission_classes = (IsAuthenticated, ApprovedUserAccessPermission, TeacherAccessPermission,)

    def post(self, request, format=None):
        serialized = CourseParticipantApproveSerializer(data=self.request.data)
        if serialized.is_valid(raise_exception=True):
            course = serialized.validated_data['course']
            if course.teacher_id == self.request.user.id:
                serialized.approve()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)


class AssignmentsList(generics.ListAPIView):
    permissions_classes = (IsAuthenticated, ApprovedUserAccessPermission, StudentAccessPermission,)

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return Assignment.objects.none()
        queryset = Assignment.objects.all()
        queryset = queryset.filter(course__participants__student=self.request.user.id) | queryset.filter(
            course__teacher=self.request.user.id)
        return queryset.order_by('-created')

    serializer_class = AssignmentSerializer


class CreateSubmissionView(APIView):
    permission_classes = [IsAuthenticated, ApprovedUserAccessPermission, StudentAccessPermission, ]

    def post(self, request, task, format=None):
        task = Task.objects.get(pk=task)
        course_participant = CourseParticipant.objects.get(student_id=self.request.user.id,
                                                           course_id=task.assignment.course)
        serialized = SubmissionPostSerializer(data={
            'task': task.id,
            'course_participant': course_participant.id
        })
        if serialized.is_valid(raise_exception=True):
            submission = serialized.create(serialized.validated_data)
            profile = get_profile(request.user)
            if profile is None or not course_participant.is_approved:
                return Response(status=403, data={'detail': 'Access forbidden'})
            grade.apply_async(
                kwargs={'course_participant_ids': [course_participant.id], 'submission_ids': [submission.id]})
            return Response(status=200, data={'detail': 'Grade started'})


class SubmissionListView(generics.ListAPIView):
    permissions_classes = (IsAuthenticated, ApprovedUserAccessPermission, StudentAccessPermission,)

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return Submission.objects.none()
        queryset = Submission.objects.filter(
            course_participant__student_id=get_profile(self.request.user).id) | Submission.objects.filter(
            course_participant__course__teacher_id=get_profile(self.request.user).id)
        return queryset.order_by('-id')

    serializer_class = SubmissionRetrieveSerializer


class MyParticipationsListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, ApprovedUserAccessPermission, StudentAccessPermission)

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return CourseParticipant.objects.none()
        return CourseParticipant.objects.filter(student_id=self.request.user.id)

    serializer_class = CourseParticipantSerializer
