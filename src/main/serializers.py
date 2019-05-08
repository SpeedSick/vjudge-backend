from rest_framework import serializers

from authentication.models import Profile
from .models import Course, CourseParticipant, Assignment, Task, Result, Submission


class CourseSerializer(serializers.ModelSerializer):
    created = serializers.DateField(required=False)
    modified = serializers.DateField(required=False)

    class Meta:
        model = Course
        fields = ('id', 'name', 'description', 'created', 'modified')

    def create(self, validated_data):
        teacher = self.context['request'].user
        return Course.objects.create(**validated_data, teacher=teacher)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance


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
        if 'student' in validated_data:
            validated_data.pop('student')

        return CourseParticipant.objects.create(**validated_data, student=user)


class AssignmentSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(many=False, queryset=Course.objects.all())
    created = serializers.DateField(required=False)
    modified = serializers.DateField(required=False)
    deadline = serializers.DateField(required=False)

    class Meta:
        model = Assignment
        fields = ('id', 'course', 'name', 'description', 'deadline', 'created', 'modified',)

    def create(self, validated_data):
        return Assignment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.deadline = validated_data.get('deadline', instance.deadline)
        instance.save()
        return instance


class TaskSerializer(serializers.ModelSerializer):
    created = serializers.DateField(required=False)
    modified = serializers.DateField(required=False)

    class Meta:
        model = Task
        fields = '__all__'

    def create(self, validated_data):
        return Task.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance


class ResultSerializer(serializers.ModelSerializer):
    submission = serializers.PrimaryKeyRelatedField(queryset=Submission.objects.all(), many=False)
    created = serializers.DateTimeField(required=False)

    class Meta:
        model = Result
        fields = ('submission', 'score', 'created')

    def create(self, validated_data):
        result = Result.objects.create(
            submission=validated_data['submission'],
            score=validated_data['score']
        )
        return result
