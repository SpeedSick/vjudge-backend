from rest_framework import permissions

from authentication.models import Profile


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
        return not profile.is_provider


class TeacherAccessPermission(permissions.BasePermission):
    message = 'Teachers are allowed'

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        profile = Profile.objects.filter(pk=request.user.id).last()
        return profile.is_provider


class ApprovedParticipantAccessPermission(permissions.BasePermission):
    message = 'Approved course participants are allowed'

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return True
