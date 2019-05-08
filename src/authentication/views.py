from rest_framework import permissions, viewsets

from authentication.models import User
from authentication.serializers import UserSerializer, UserPostSerializer


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
