from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework import permissions

from authentication.models import User, Profile
from authentication.serializers import UserSerializer


class UserCreateAPIView(CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRetrieveAPIView(RetrieveAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserListAPIView(ListAPIView):
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        queryset = User.objects.filter(pk=self.request.user.id)
        return queryset

    serializer_class = UserSerializer
