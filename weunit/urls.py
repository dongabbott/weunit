# -*-coding:utf-8 -*-
"""webapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from rest_framework import routers
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer
from account import views as account_view
from project import views as project_view
from backend import views as apitest_view


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', account_view.UserViewSet)
router.register(r'groups', account_view.GroupViewSet)


schema_view = get_schema_view(title='测试系统接口', renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer])

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/account/', include(router.urls)),
    url(r'^api/account/login', account_view.login),
    url(r'^api/account/userinfo/', account_view.account),
    url(r'^api/account/logout', account_view.logout),
    url(r'^docs/', schema_view, name=u'接口文档'),
    url(r'^$', TemplateView.as_view(template_name="index.html")),
    url(r'^api/project/$', project_view.ProjectList.as_view()),
    url(r'^api/project/(?P<pk>[0-9]+)/$', project_view.ProjectDetail.as_view()),
    url(r'^api/project/setting/(?P<pk>[0-9]+)/$', project_view.SettingDetail.as_view()),
    url(r'^api/project/ready/$', project_view.xunit_init),
    url(r'^api/apitest/users/$', apitest_view.apiTokenUserList.as_view()),
    url(r'^api/apitest/users/refresh/$', apitest_view.refresh),
    url(r'^api/apitest/users/(?P<pk>[0-9]+)/$', apitest_view.apiTokenUserDetail.as_view()),
    url(r'^api/apitest/case/$', apitest_view.apiTestCaseList.as_view()),
    url(r'^api/apitest/case/(?P<pk>[0-9]+)/$', apitest_view.apiTestCaseDetail.as_view()),
    url(r'^api/apitest/case/debug/$', apitest_view.http_remote),
    url(r'^api/apitest/suite/$', apitest_view.testSuiteList.as_view()),
]
