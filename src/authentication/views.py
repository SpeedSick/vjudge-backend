from django.db.models import Q
from rest_framework import permissions, viewsets, generics

from authentication.models import User
from authentication.serializers import UserSerializer, UserPostSerializer
from main.permissions import TeacherAccessPermission


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        queryset = User.objects.all()
        if self.action in ('list', 'update', 'partial_update', 'destroy'):
            if self.request.user:
                queryset = queryset.filter(pk=self.request.user.id)
            else:
                queryset = queryset.none()
        return queryset

    def get_serializer_class(self):
        serializer_class = UserSerializer
        if self.action in ('update', 'partial_update',):
            serializer_class = UserPostSerializer
        return serializer_class


class StudentsListView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = User.objects.filter(profile__is_teacher=False)
    serializer_class = UserSerializer


class TeachersListView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = User.objects.filter(Q(profile__is_teacher=True) & Q(profile__is_approved=True))
    serializer_class = UserSerializer
