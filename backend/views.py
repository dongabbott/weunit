# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404
from rest_framework import permissions
from rest_framework.decorators import permission_classes, authentication_classes
from .models import ApiTestCases, ApiTokenUser
from .serializers import apiTokenUserSerializers, apiTestCaseSerializers
from rest_framework import generics
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from .utils.weclient import WeHttpClient
from project.models import Projects, Settings
from project.serializers import SettingSerializer


class apiTokenUserList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    queryset = ApiTokenUser.objects.all()
    serializer_class = apiTokenUserSerializers
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username', 'user_desc')

    def post(self, request, format=None):
        serializer = apiTokenUserSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class apiTokenUserDetail(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get_object(self, pk):
        try:
            return ApiTokenUser.objects.get(pk=pk)
        except ApiTokenUser.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = apiTokenUserSerializers(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = apiTokenUserSerializers(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class apiTestCaseList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    queryset = ApiTestCases.objects.all()
    serializer_class = apiTestCaseSerializers
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'suite_name', 'func_name')

    def post(self, request, format=None):
        serializer = apiTestCaseSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save(user_id=request.user.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class apiTestCaseDetail(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get_object(self, pk):
        try:
            return ApiTestCases.objects.get(pk=pk)
        except ApiTestCases.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = apiTestCaseSerializers(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = apiTestCaseSerializers(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
@authentication_classes([TokenAuthentication, SessionAuthentication, ])
@permission_classes([IsAuthenticated, ])
def http_remote(request):
    url = request.data.get("url")
    params = request.data.get("params")
    params = eval(params) if params != '' else None
    method = request.data.get("method")
    headers = request.data.get("headers")
    headers = eval(headers) if headers != '' else None
    user_id = request.data.get("user_id")
    if user_id:
        user = ApiTokenUser.objects.get(pk=user_id)
        headers['Authorization'] = user.token_value
    try:
        data = WeHttpClient(url, params=params, headers=headers).result(method=method)
        return Response({'data': data})
    except Exception, err:
        print Response({'error': err})


@api_view(["POST"])
@authentication_classes([TokenAuthentication, SessionAuthentication, ])
@permission_classes([IsAuthenticated, ])
def refresh(request):
    user_id = request.data.get("user_id")
    try:
        test_user = ApiTokenUser.objects.get(pk=int(user_id))
    except ApiTokenUser.DoesNotExist:
        raise Http404
    user_arg = dict([test_user.username.split("="), test_user.password.split("=")])
    settings = Settings.objects.filter(project_id=test_user.project_id)
    print '7777777777777777777777', settings
    for setting in settings:
        print '888888888888888888'
        print 'gggggggggggggggggg', setting.setting_type
        if setting.setting_type == 0:
            base_url = setting.setting_value
            next()
        elif setting.setting_type == 1:
            print "ggggggggggggg1111111"
            base_header = setting.setting_value
        elif setting.setting_type == 4:
            login_url = setting.setting_value
            print "dddddddd", login_url
        elif setting.setting_type == 5:
            login_base_arg = setting.setting_value
        elif setting.setting_type == 6:
            login_get_token = setting.setting_value
        data = WeHttpClient(base_url + login_url,
                            params=dict(user_arg.items() + eval(login_base_arg).items()),
                            headers=base_header).result(method="POST")
        print data