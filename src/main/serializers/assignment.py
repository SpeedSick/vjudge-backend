from rest_framework import serializers

from main.models import Course, Assignment


class AssignmentSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(many=False, queryset=Course.objects.all())
    created = serializers.DateField(required=False)
    modified = serializers.DateField(required=False)
    deadline = serializers.DateTimeField(required=False)

    class Meta:
        model = Assignment
        fields = (
            'id', 'course', 'name', 'description', 'deadline', 'folder_name', 'created', 'git_fork_link', 'modified',)

    def create(self, validated_data):
        return Assignment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.deadline = validated_data.get('deadline', instance.deadline)
        instance.save()
        return instance
