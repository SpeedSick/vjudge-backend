from rest_framework import serializers

from main.models import Task
from .submission import SubmissionSerializer
from .result import ResultSerializer


class TaskSerializer(serializers.ModelSerializer):
    created = serializers.DateField(required=False)
    modified = serializers.DateField(required=False)
    submissions = SubmissionSerializer(many=True, required=False)

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
