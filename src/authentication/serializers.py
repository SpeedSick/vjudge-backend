from rest_framework import serializers

from authentication.models import Profile, User


class ProfileSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=False)

    class Meta:
        model = Profile
        exclude = ('user', 'is_approved', 'git_username',)

    def update(self, instance, validated_data):
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.save()
        return


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
        user.save()
        Profile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        if 'profile' in validated_data:
            profile_data = validated_data.pop('profile')
            profile = Profile.objects.get(pk=instance.id)
            serialized = ProfileSerializer(data=profile_data)
            if serialized.is_valid():
                serialized.update(profile, serialized.validated_data)
            profile.user = instance
            profile.save()

        instance.first_name = validated_data.get('first_name')
        instance.last_name = validated_data.get('last_name')
        instance.save()
        return instance
