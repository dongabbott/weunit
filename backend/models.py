# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from project.models import Projects
from django.conf import settings
# Create your models here.


class ApiTokenUser(models.Model):
    username = models.CharField(u"用户名", max_length=32, null=False)
    password =  models.CharField(u"密码", max_length=50, null=False)
    user_desc = models.TextField(u"用户描述", max_length=200)
    token_api = models.CharField(u"获取token的api", max_length=100)
    token_value = models.CharField(u"用例名称", max_length=150)
    token_term = models.BigIntegerField(u"token有效期")
    create_time = models.DateField(u"创建时间", auto_now=True)
    update_time = models.DateField(u"更新时间", auto_now_add=True)

    class Meta:
        db_table = "testuser"

    def __unicode__(self):
        return "%s%s" %(self.username, self.user_desc)



class ApiTestCases(models.Model):
    name = models.CharField(u"用例名称", max_length=50)
    description = models.TextField(u"描述")
    suite_name = models.CharField(u"unittest套件名", max_length=30)
    func_name = models.CharField(u"unittest方法名", max_length=30)
    REQUEST_METHOD = (
        (1, 'GET'),
        (2, 'POST'),
        (3, 'PUT'),
        (4, 'DELETE')
    )
    method = models.IntegerField(u"请求方法", choices=REQUEST_METHOD)
    uri = models.CharField(u"请求地址", max_length=100)
    is_token = models.BooleanField(u"是否需要token")
    HEADER_DEFAULT = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                      "Accept": "application/vnd.timehut.v5+json",
                      "User-Agent": "com.liveyap.timehut/5.1.1.2 (android 7.1.1, OD105) (SOURCE/aliyun, VERSION_CODE/227)"
                      }
    token_user = models.ForeignKey(ApiTokenUser, related_name="token_user", blank=True)
    params = models.CharField(u"请求体", max_length=500)
    headers = models.CharField(u"请求头", max_length=500)
    project = models.ForeignKey(Projects, related_name="project", null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    create_time = models.DateTimeField(u'创建时间', auto_now=True)
    update_time = models.DateField(u"更新时间", auto_now_add=True)


    class Meta:
        db_table = "apicase"

    def __unicode__(self):
        return self.name
