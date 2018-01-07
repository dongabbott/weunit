# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from project.models import Projects
from django.conf import settings
# Create your models here.


class ApiTokenUser(models.Model):
    user_desc = models.CharField(u"用户描述", max_length=30)
    token_api = models.CharField(u"用例名称", max_length=30)
    token_value = models.CharField(u"用例名称", max_length=150)



class ApiTestCases(models.Model):
    name = models.CharField(u"用例名称", max_length=50)
    description = models.TextField(u"描述")
    suite_name = models.CharField(u"unittest套件名", max_length=30)
    func_name = models.CharField(u"unittest方法名", max_length=30)
    REQUEST_METHOD = (
        (1, 'get'),
        (2, 'post'),
        (3, 'put'),
        (4, 'patch')
    )
    method = models.CharField(u"请求方法", choices=REQUEST_METHOD)
    uri = models.CharField(u"请求地址", max_length=100)
    is_token = models.BooleanField(u"是否需要token")
    HEADER_DEFAULT = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                      "Accept": "application/vnd.timehut.v5+json",
                      "User-Agent": "com.liveyap.timehut/5.1.1.2 (android 7.1.1, OD105) (SOURCE/aliyun, VERSION_CODE/227)"
                      }
    token_user = models.ForeignKey(ApiTokenUser, null=True)
    params = models.TextField(u"请求体")
    headers = models.CharField(u"请求头")
    project = models.ForeignKey(Projects, null=True)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
