from django.contrib.auth.models import User
from rest_framework import serializers

from authentication.serializers import UserSerializer
from main.models import Course, News
from main.serializers import AssignmentSerializer
from main.utils import get_or_create_course_participant


class CoursePostSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    image = serializers.ImageField(required=False)
    participants = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all(), required=False)

    class Meta:
        model = Course
        fields = ('id', 'name', 'description', 'participants', 'image')

    def create(self, validated_data):
        teacher = self.context['request'].user
        participants_data = None
        if 'participants' in validated_data:
            participants_data = validated_data.pop('participants')
        course = Course.objects.create(**validated_data, teacher=teacher)
        if participants_data:
            for student in participants_data:
                get_or_create_course_participant(course.id, student.id)
        return course

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        if 'participants' in validated_data:
            for student in validated_data['participants']:
                get_or_create_course_participant(instance.id, student.id)
        return instance


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ('message',)


class CourseGetSerializer(serializers.ModelSerializer):
    teacher = UserSerializer()
    notifications = serializers.SerializerMethodField()

    def get_notifications(self, instance):
        return [NewsSerializer(instance=x).data for x in
                instance.notifications.filter(user=self.context['request'].user)]

    class Meta:
        model = Course
        fields = (
            'id', 'teacher', 'name', 'description', 'created', 'modified', 'students', 'image', 'notifications',)


class CourseRetrieveSerializer(serializers.ModelSerializer):
    assignments = AssignmentSerializer(many=True)
    notifications = serializers.SerializerMethodField()

    def get_notifications(self, instance):
        return [NewsSerializer(instance=x).data for x in
                instance.notifications.filter(user=self.context['request'].user)]

    class Meta:
        model = Course
        fields = (
            'id', 'teacher', 'name', 'description', 'created', 'modified', 'students', 'image', 'assignments',
            'notifications',)
