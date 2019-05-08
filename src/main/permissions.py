from rest_framework import permissions

from authentication.models import Profile
from core import settings


class ApprovedUserAccessPermission(permissions.BasePermission):
    message = 'Approved are allowed'

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        profile = Profile.objects.filter(pk=request.user.id).last()
        return profile.is_approved


class StudentAccessPermission(permissions.BasePermission):
    message = 'Students are allowed'

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        profile = Profile.objects.filter(pk=request.user.id).last()
        return not profile.is_teacher


class TeacherAccessPermission(permissions.BasePermission):
    message = 'Teachers are allowed'

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        profile = Profile.objects.filter(pk=request.user.id).last()
        return profile.is_teacher


class ApprovedParticipantAccessPermission(permissions.BasePermission):
    message = 'Approved course participants are allowed'

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return True


class CustomTokenPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return settings.X_API_KEY == request.META.get('HTTP_X_API_KEY')
