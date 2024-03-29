from rest_framework import serializers

from main.models import Submission, Task, CourseParticipant
from .course_participant import CourseParticipantSerializer
from .result import ResultSerializer


class SubmissionPostSerializer(serializers.ModelSerializer):
    task = serializers.PrimaryKeyRelatedField(many=False, queryset=Task.objects.all())
    course_participant = serializers.PrimaryKeyRelatedField(many=False, queryset=CourseParticipant.objects.all())

    class Meta:
        model = Submission
        fields = ('task', 'course_participant',)

    def create(self, validated_data):
        return Submission.objects.create(**validated_data)


class SubmissionSerializer(serializers.ModelSerializer):
    task = serializers.PrimaryKeyRelatedField(many=False, queryset=Task.objects.all())
    course_participant = CourseParticipantSerializer()
    results = ResultSerializer(required=False, many=True)

    class Meta:
        model = Submission
        fields = ('task', 'course_participant', 'results',)

    def create(self, validated_data):
        return Submission.objects.create(**validated_data)


class SubmissionRetrieveSerializer(serializers.ModelSerializer):
    results = ResultSerializer(many=True)

    class Meta:
        model = Submission
        fields = ('results', 'task',)
