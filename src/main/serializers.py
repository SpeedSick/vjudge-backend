from rest_framework import serializers
from .models import Course, CourseParticipant, Assignment, Task


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
        student = self.context['request'].user
        return CourseParticipant.objects.create(**validated_data, student=student)


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


class TaskSerializer(serializers.Serializer):
    created = serializers.DateField(required=False)
    modified = serializers.DateField(required=False)

    class Meta:
        model = Task

    def create(self, validated_data):
        return Assignment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance