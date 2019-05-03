from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework import permissions, mixins, viewsets

from authentication.models import User, Profile
from authentication.serializers import UserSerializer


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

    serializer_class = UserSerializer
