import datetime

from django.contrib.auth import authenticate
from django.db.models import Q
from rest_framework import permissions, viewsets, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import User, PasswordResetToken
from authentication.serializers import UserSerializer, UserPostSerializer, ChangePasswordSerializer, EmailSerializer
from authentication.utils import send_text, gen_password
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


class PasswordChangeView(APIView):
    def post(self, request, format=None):
        serialized = ChangePasswordSerializer(data=request.data)
        if request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if serialized.is_valid():
            user = authenticate(
                username=request.user.username,
                password=serialized.validated_data['password'],
            )
            if user == self.request.user:
                user.set_password(serialized.validated_data['new_password'])
                user.save()
                return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(APIView):
    def post(self, request, format=None):
        serialized = EmailSerializer(data=request.data)
        if serialized.is_valid():
            users = User.objects.filter(email=serialized.validated_data['email'])
            for user in users:
                token = PasswordResetToken.objects.create(user=user)
                url = request.build_absolute_uri(request.get_full_path())
                send_text(
                    serialized.validated_data['email'],
                    'Сброс пароля для KBTU Virtual Judge',
                    u'''Вы получили это сообщение, потому что кто-то запросил сброс пароля для вашего аккаунта\n
Если это были не вы, проигнорируйте это сообщение\n
Ссылка для сброса пароля {}{}/\n'''.format(url, token.token)
                )
            return Response({'status': 'done'})


class PasswordResetConfirmView(APIView):
    def get(self, request, reset_token, format=None):
        day_ago = datetime.datetime.now() - datetime.timedelta(1)
        tokens = PasswordResetToken.objects.filter(Q(token=reset_token) & Q(created__gte=day_ago))
        if tokens.count():
            for token in tokens:
                new_password = gen_password()
                token.user.set_password(raw_password=new_password)
                token.user.save()
                send_text(
                    token.user.email,
                    'Сброс пароля для KBTU Virtual Judge',
                    u"""Ваш новый пароль {}\n
Он будет активен в течении 24 часов, смените пароль в настройках""".format(new_password)
                )
        return Response({'status': 'done'})
