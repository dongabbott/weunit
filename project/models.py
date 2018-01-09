# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.db import models
import uuid

# Create your models here.
<<<<<<< HEAD
SETTING_CLASS = [
    (0, u"服务地址"),
    (1, u"请求头"),
    (2, u"默认参数"),
    (3, u"数据库")
]

class Projects(models.Model):
    project_name = models.CharField(u'项目名称', max_length=30, blank=False)
    project_desc = models.CharField(u'项目描述', max_length=200)
    project_title = models.CharField(u'项目简称', max_length=20, blank=False)
    project_root = models.CharField(u'项目根目录', max_length=200, )
    project_status = models.BooleanField(u'项目状态', null=False, default=True)
    project_key = models.CharField(u'项目key', max_length=20)
=======


class Projects(models.Model):
    project_name = models.CharField(u'项目名称', max_length=30)
    project_desc = models.CharField(u'项目描述', max_length=200, blank=True)
    project_title = models.CharField(u'项目简称', max_length=20)
    project_root = models.CharField(u'项目根目录', max_length=200, )
    project_status = models.BooleanField(u'项目状态', null=False, default=True)
    project_key = models.CharField(u'项目key', max_length=20, null=True)
>>>>>>> b78ac6aaf3e44afdecffbf5c2a223debce6b3ea4
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    class Meta:
        db_table = "projects"

    def __unicode__(self):
        return self.project_name


class Settings(models.Model):
<<<<<<< HEAD

    setting_type = models.IntegerField(u"配置类型")
    setting_value = models.TextField(u"配置值", max_length=500)
    setting_desc = models.TextField(u"配置描述", max_length=500)
=======
    headers = models.TextField("请求头", blank=True)
    params = models.TextField("默认请求参数", blank=True)
    db_connect = models.CharField("数据库连接信息", max_length=100, blank=True)
    address = models.URLField("数据库连接信息", max_length=100, blank=True)
>>>>>>> b78ac6aaf3e44afdecffbf5c2a223debce6b3ea4
    project = models.ForeignKey(Projects, related_name=u'setting', blank=True)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)

    class Meta:
        db_table = "project_settings"

    def __unicode__(self):
        return self.address


class Tasks(models.Model):
    task_id = models.UUIDField(default=uuid.uuid4, null=False)
    project = models.ForeignKey(Projects, related_name=u'task')
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    start_time = models.DateTimeField(u'开始时间', null=True)
    stop_time = models.DateTimeField(u'开始时间', null=True)

    class Meta:
        db_table = 'test_task'
