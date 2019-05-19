from rest_framework import generics, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from authentication.models import Profile, User
from grader.tasks import check_submissions
from main.models import News, Submission
from main.serializers.course import CourseRetrieveSerializer
from main.serializers.course_participant import CourseParticipantApproveSerializer, CourseParticipantUpdateSerializer
from main.serializers.submission import SubmissionSerializer, SubmissionRetrieveSerializer
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
        serializer_class = CourseRetrieveSerializer
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            serializer_class = CoursePostSerializer
        elif self.action == 'retrieve':
            serializer_class = CourseRetrieveSerializer
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
            queryset = queryset.filter(course__participants__student=self.request.user.id)
            print(queryset)
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

    def post(self, request, format=None):
        task = Task.objects.get(pk=self.request.data['task'])
        course_participant = CourseParticipant.objects.get(student_id=self.request.user.id,
                                                           course_id=task.assignment.course)
        serialized = SubmissionSerializer(data={
            'task': task.id,
            'course_participant': course_participant.id
        })
        if serialized.is_valid(raise_exception=True):
            submission = serialized.create(serialized.validated_data)
            profile = get_profile(request.user)
            if profile is None or not profile.is_teacher or submission.task.assignment.course.teacher_id != profile.id:
                return Response(status=403, data={'detail': 'Access forbidden'})
            check_submissions.apply_async(kwargs={'submission_ids': submission.pk})
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
