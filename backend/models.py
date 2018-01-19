# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from project.models import Projects
from django.conf import settings
from .utils.options import REQUEST_METHOD, HEADER_DEFAULT
# Create your models here.


class ApiTokenUser(models.Model):
    username = models.CharField(u"用户名", max_length=32, null=False)
    password = models.CharField(u"密码", max_length=50, null=False)
    user_desc = models.CharField(u"用户描述", max_length=200)
    token_value = models.CharField(u"token值", max_length=200)
    token_term = models.BigIntegerField(u"token有效期")
    project = models.ForeignKey(Projects, null=True)
    create_time = models.DateField(u"创建时间", auto_now=True)
    update_time = models.DateField(u"更新时间", auto_now_add=True)


    class Meta:
        db_table = "testuser"

    def __unicode__(self):
        return "%s%s" % (self.username, self.user_desc)


class ApiTestCases(models.Model):
    name = models.CharField(u"用例名称", max_length=50)
    description = models.TextField(u"描述")
    suite_name = models.CharField(u"unittest套件名", max_length=30)
    func_name = models.CharField(u"unittest方法名", max_length=30)
    method = models.IntegerField(u"请求方法", choices=REQUEST_METHOD)
    uri = models.CharField(u"请求地址", max_length=100)
    is_token = models.BooleanField(u"是否需要token")
    params = models.CharField(u"请求体", max_length=500)
    headers = models.CharField(u"请求头", max_length=500, default=HEADER_DEFAULT)
    project = models.ForeignKey(Projects, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    create_time = models.DateTimeField(u'创建时间', auto_now=True)
    update_time = models.DateField(u"更新时间", auto_now_add=True)

    class Meta:
        db_table = "apicase"

    def __unicode__(self):
        return self.name


class TestApiUser(models.Model):
    case = models.ForeignKey(ApiTestCases)
    token_user = models.ForeignKey(ApiTokenUser)
    create_time = models.DateTimeField(u'创建时间', auto_now=True)
    update_time = models.DateField(u"更新时间", auto_now_add=True)

    class Meta:
        db_table = "apiuser"