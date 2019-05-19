from rest_framework import serializers

from main.models import Submission, Result


class ResultSerializer(serializers.ModelSerializer):
    submission = serializers.PrimaryKeyRelatedField(queryset=Submission.objects.all(), many=False)
    created = serializers.DateTimeField(required=False)

    class Meta:
        model = Result
        fields = ('submission', 'score', 'created',)

    def create(self, validated_data):
        result = Result.objects.create(
            submission=validated_data['submission'],
            score=validated_data['score']
        )
        return result
