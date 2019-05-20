from rest_framework import serializers

from main.models import Task, Submission
from .submission import SubmissionSerializer
from .result import ResultSerializer


class TaskSerializer(serializers.ModelSerializer):
    created = serializers.DateField(required=False)
    modified = serializers.DateField(required=False)
    my_percentage = serializers.SerializerMethodField(required=False)
    submissions = SubmissionSerializer(many=True, required=False)

    def get_my_percentage(self, instance):
        if self.context['request'].user.is_anonymous:
            return None
        submission = instance.submissions.filter(course_participant__student=self.context['request'].user.id).last()
        if submission is None:
            return None
        result = submission.results.last()
        if result is None:
            return None
        return result.score

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
