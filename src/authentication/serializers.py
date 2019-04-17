from rest_framework import serializers

from authentication.models import Profile


class ProfileSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = Profile
        fields = ('id', 'username', 'first_name', 'email', 'last_name', 'password',
                  'is_teacher', 'is_student',)


    def validate(self, data):
        is_student = data.get('is_student')
        is_teacher = data.get('is_teacher')
        if not (is_student is None) and is_student == is_teacher:
            raise serializers.ValidationError('User must be either student or teacher')
        return data

    def create(self, validated_data):
        password_data = validated_data.pop('password')
        profile = Profile.objects.create(**validated_data, is_approved=False)
        profile.set_password(password_data)
        profile.save()
        return profile
