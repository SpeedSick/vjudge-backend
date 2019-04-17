from rest_framework.generics import CreateAPIView
from rest_framework import permissions

from authentication.models import Profile
from authentication.serializers import ProfileSerializer


class ProfileCreateAPIView(CreateAPIView):

    permission_classes = (permissions.AllowAny,)
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
