# -*-coding:utf-8 -*-

from .models import Projects, Settings, Tasks
from rest_framework import serializers
import random, string
from django.conf import settings
import os


def project_accesskey(number=15):
    '''随机生成一个唯一字符串
    '''
    access_key = ''
    for _ in xrange(0, number):
        access_key += random.choice(string.ascii_letters + string.digits)
    return access_key


class SettingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Settings
        fields = ('id', 'setting_type', 'setting_value', 'setting_desc', 'create_time', 'setting_type')
        related_fields = ['project_id']


class ProjectSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(max_length=20)
    project_desc = serializers.CharField(max_length=200)
    project_title = serializers.CharField(max_length=20)
    project_root = serializers.CharField(max_length=200, required=False)
    project_status = serializers.BooleanField(required=False)
    setting = SettingSerializer(required=False, many=True)

    def to_internal_value(self, value):
        # setting中空字符验证的除去
        return value

    class Meta:
        model = Projects
        fields = ('id', 'project_name', 'project_desc',
                  'project_status', 'project_key', 'create_time', 'setting',
                  'user_id', 'project_root', 'project_title'
                  )

    def validate(self, data):
        if data.get('project_key') is None:
            data['project_key'] = project_accesskey()
        if data['project_root'] == '':
            data['project_root'] = os.path.join(settings.BASE_DIR, 'test_project', data['project_title'])
        return data

    def create(self, validated_data):
        validated_data.pop('setting')
        project = Projects.objects.create(**validated_data)
        return project

    def update(self, instance, validated_data):
        settings_data = validated_data.pop('setting')
        instance.project_name = validated_data.get('project_name', instance.project_name)
        instance.project_desc = validated_data.get('project_desc', instance.project_desc)
        instance.project_title = validated_data.get('project_title', instance.project_title)
        instance.project_root = validated_data.get('project_root', instance.project_root)
        instance.project_status = validated_data.get('project_status', instance.project_status)
        instance.save()
        for setting_data in settings_data:
            setting_id = setting_data.get('id')
            if setting_data.get('id') is None:
                setting_data['project_id'] = instance.id
                Settings.objects.create(**setting_data)
            else:
                Settings.objects.filter(id=setting_id).update(**setting_data)
        return instance


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = ('id', 'task_id', 'project_id', 'create_time', 'start_time', 'stop_time')
