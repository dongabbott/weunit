# -*-coding:utf-8 -*-

<<<<<<< HEAD
from .models import Projects, Settings, Tasks, SETTING_CLASS
=======
from .models import Projects, Settings, Tasks
>>>>>>> b78ac6aaf3e44afdecffbf5c2a223debce6b3ea4
from rest_framework import serializers
import random, string, datetime
from django.conf import settings
import os, json


def project_accesskey(number=15):
    '''随机生成一个唯一字符串
    '''
    access_key = ''
    for _ in xrange(0, number):
        access_key += random.choice(string.ascii_letters + string.digits)
    return access_key


class SettingSerializer(serializers.ModelSerializer):
<<<<<<< HEAD

    class Meta:
        model = Settings
        fields = ('id', 'setting_type', 'setting_value', 'setting_desc', 'create_time', 'setting_type')
=======
    headers = serializers.CharField(max_length=500, required=False, allow_blank=True)
    params = serializers.CharField(max_length=800, required=False, allow_blank=True)
    address = serializers.CharField(max_length=200, required=False, allow_blank=True)
    db_connect = serializers.CharField(max_length=200, required=False, allow_blank=True)

    class Meta:
        model = Settings
        fields = ('id', 'headers', 'params', 'db_connect', 'address', 'project_id', 'create_time')
>>>>>>> b78ac6aaf3e44afdecffbf5c2a223debce6b3ea4
        related_fields = ['project_id']


class ProjectSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(max_length=20)
    project_desc = serializers.CharField(max_length=200)
    project_title = serializers.CharField(max_length=20)
<<<<<<< HEAD
    project_root = serializers.CharField(max_length=200, required=False)
    project_status = serializers.BooleanField(required=False)
    setting = SettingSerializer(required=False, many=True)
=======
    project_root = serializers.CharField(max_length=200, required=False, allow_blank=True)
    project_status = serializers.BooleanField(required=False)
    setting = SettingSerializer(required=False)
>>>>>>> b78ac6aaf3e44afdecffbf5c2a223debce6b3ea4

    def to_internal_value(self, value):
        return value

<<<<<<< HEAD
=======

>>>>>>> b78ac6aaf3e44afdecffbf5c2a223debce6b3ea4
    class Meta:
        model = Projects
        fields = ('id', 'project_name', 'project_desc',
                  'project_status', 'project_key', 'create_time', 'setting',
                  'user_id', 'project_root', 'project_title'
                  )

    def validate(self, data):
<<<<<<< HEAD
=======
        print "333333333", data.get('setting')
>>>>>>> b78ac6aaf3e44afdecffbf5c2a223debce6b3ea4
        if data.get('project_key') is None:
            data['project_key'] = project_accesskey()
        if data['project_root'] == '':
            data['project_root'] = os.path.join(settings.BASE_DIR, 'test_project', data['project_title'])
<<<<<<< HEAD
        return data

    def create(self, validated_data):
        validated_data.pop('setting')
        project = Projects.objects.create(**validated_data)
        return project

    def update(self, instance, validated_data):
        settings_data = validated_data.pop('setting')
=======
        if data['setting'] is not None:
            data['setting'] = json.loads(data['setting'])
        print '55555555555', data['setting']
        return data

    def create(self, validated_data):
        print 22222222222, validated_data
        project_settings = validated_data.pop('setting')
        project = Projects.objects.create(**validated_data)
        project_settings['project_id'] = project.id
        setting = Settings.objects.update_or_create(**project_settings)
        return project

    def update(self, instance, validated_data):
        print 444444444, validated_data
>>>>>>> b78ac6aaf3e44afdecffbf5c2a223debce6b3ea4
        instance.project_name = validated_data.get('project_name', instance.project_name)
        instance.project_desc = validated_data.get('project_desc', instance.project_desc)
        instance.project_title = validated_data.get('project_title', instance.project_title)
        instance.project_root = validated_data.get('project_root', instance.project_root)
        instance.project_status = validated_data.get('project_status', instance.project_status)
<<<<<<< HEAD
        instance.save()
        for setting_data in settings_data:
            setting_id = setting_data.get('id')
            if setting_data.get('id') is None:
                setting_data['project_id'] = instance.id
                Settings.objects.create(**setting_data)
            else:
                Settings.objects.filter(id=setting_id).update(**setting_data)
=======
        instance.setting = validated_data.get('setting', instance.setting)
        instance.save()
>>>>>>> b78ac6aaf3e44afdecffbf5c2a223debce6b3ea4
        return instance


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = ('id', 'task_id', 'project_id', 'create_time', 'start_time', 'stop_time')
