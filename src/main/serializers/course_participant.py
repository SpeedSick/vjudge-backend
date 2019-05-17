from django.contrib.auth.models import User
from rest_framework import serializers

from authentication.models import Profile
from main.models import CourseParticipant, Course


class CourseParticipantSerializer(serializers.ModelSerializer):
    joined = serializers.DateField(required=False)
    course = serializers.PrimaryKeyRelatedField(many=False, queryset=Course.objects.all())

    class Meta:
        model = CourseParticipant
        exclude = ('is_approved',)

    def create(self, validated_data):
        user = self.context['request'].user
        user_profile = Profile.objects.get(id=user.id)
        if not user_profile.is_teacher:
            user = validated_data.pop('student')
        else:
            validated_data['is_approved'] = True
        if 'student' in validated_data:
            validated_data.pop('student')

        return CourseParticipant.objects.create(**validated_data, student=user)

    def update(self, instance, validated_data):
        user = self.context['request'].user
        user_profile = Profile.objects.get(id=user.id)
        if user_profile.is_teacher and user.id == instance.course.teacher_id:
            instance.is_approved = True
        instance.save()
        return instance


class CourseParticipantUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseParticipant
        fields = ('git_repository_name',)

    def update(self, instance, validated_data):
        instance.git_repository_name = validated_data.get('git_repository_name', instance.git_repository_name)
        instance.save()
        return instance


class CourseParticipantApproveSerializer(serializers.Serializer):
    student = serializers.PrimaryKeyRelatedField(many=False, queryset=User.objects.all())
    course = serializers.PrimaryKeyRelatedField(many=False, queryset=Course.objects.all())

    def approve(self):
        course_participant, created = CourseParticipant.objects.get_or_create(student=self.validated_data['student'],
                                                                              course=self.validated_data['course'])
        course_participant.is_approved = True
        course_participant.save()
        return True
