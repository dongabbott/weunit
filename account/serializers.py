from django.contrib.auth.models import User, Group
from rest_framework import serializers
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name', 'url')


class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True, read_only=True)
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = UserModel
        fields = ('id', 'url', 'username', 'email', 'groups', 'password', 'is_staff', 'is_active', 'date_joined')

    def create(self, validated_data):
        user = UserModel.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.password = validated_data.get('password', instance.password)
        instance.is_staff = validated_data.get('is_staff', instance.is_staff)
        instance.save()
        return instance