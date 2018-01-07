# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .serializers import UserSerializer, GroupSerializer
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core import serializers
from rest_framework import generics
import django_filters.rest_framework

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    """
    允许查看和编辑user 的 API endpoint
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('username', 'email', 'is_staff')


class GroupViewSet(viewsets.ModelViewSet):
    """
    允许查看和编辑group的 API endpoint
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(username=username, password=password)
    if not user:
        error = u'用户名或密码错误'
        return Response({"error": error}, status=HTTP_401_UNAUTHORIZED)
    else:
        user_info = User.objects.values('id', 'username',
                                        'email', 'first_name',
                                        'last_name', 'is_staff',
                                        'is_active', 'is_superuser').filter(username=username).first()
        if user_info.get("is_staff") is False or user_info.get("is_active") is False:
            error = u'帐户被锁定请联系管理员'
            return Response({"error": error}, status=HTTP_401_UNAUTHORIZED)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({"token": 'Token ' + token.key, 'user_info': user_info, 'code': '0000'})


@api_view(["GET"])
@permission_classes([IsAuthenticated,])
def account(request):
    current_user = request.user
    user_info = User.objects.values('id', 'username',
                                    'email', 'first_name',
                                    'last_name', 'is_staff',
                                    'is_active', 'is_superuser').filter(id=current_user.id).first()
    return Response({'user_info': user_info, 'role':['admin',]})


@api_view(["POST"])
@authentication_classes([TokenAuthentication, SessionAuthentication,])
@permission_classes([IsAuthenticated,])
def logout(request):
    current_user = request.user
    current_user.auth_token.delete()
    return Response({'success':u'退出成功'})
