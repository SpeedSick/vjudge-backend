from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from authentication.models import Profile, User


class ProfileSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=False)

    class Meta:
        model = Profile
        exclude = ('user', 'is_approved', 'git_username',)


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password', 'profile')

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        if not profile_data['is_teacher']:
            validated_data['is_approved'] = True
        user.save()
        Profile.objects.create(user=user, **profile_data)
        return user


class ProfilePostSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=False)

    class Meta:
        models = Profile
        fields = ('avatar',)

    def update(self, instance, validated_data):
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.save()
        return


class UserPostSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    profile = ProfilePostSerializer(required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'profile',)

    def update(self, instance, validated_data):
        if 'profile' in validated_data:
            profile_data = validated_data.pop('profile')
            profile = Profile.objects.get(pk=instance.id)
            serialized = ProfileSerializer(data=profile_data)
            if serialized.is_valid():
                serialized.update(profile, serialized.validated_data)
            profile.user = instance
            profile.save()

        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance


class EmailSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)

    def validate_email(self, value):
        if User.objects.filter(email=value).count() == 0:
            raise ValidationError('No user found with this email')
        return value


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
