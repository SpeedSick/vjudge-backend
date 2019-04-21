from rest_framework.generics import CreateAPIView
from rest_framework import permissions

from authentication.models import User
from authentication.serializers import UserSerializer


class ProfileCreateAPIView(CreateAPIView):

    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
