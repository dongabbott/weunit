# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404
from rest_framework import permissions
from rest_framework.decorators import permission_classes, authentication_classes
from .models import ApiTestCases, ApiTokenUser, TestSuite
from .serializers import apiTokenUserSerializers, apiTestCaseSerializers, testSuiteSerializers
from rest_framework import generics
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from .utils.weclient import WeHttpClient
from .utils.options import REQUEST_METHOD
from project.models import Settings
from django.db.models import Q


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


class testSuiteList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    serializer_class = testSuiteSerializers
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = TestSuite.objects.all()
        project_id = self.request.query_params.get('project_id')
        suite_name = self.request.query_params.get('suite_name')
        if suite_name or project_id:
            return queryset.filter(Q(project_id=project_id)|Q(suite_name__icontains = suite_name))
        else:
            return queryset

    def post(self, request, format=None):
        serializer = testSuiteSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class testSuiteDetail(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get_object(self, pk):
        try:
            return ApiTokenUser.objects.get(pk=pk)
        except ApiTokenUser.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        suite = self.get_object(pk)
        serializer = testSuiteSerializers(suite)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        suite = self.get_object(pk)
        serializer = testSuiteSerializers(suite, data=request.data)
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
    search_fields = ('name', 'project_id', 'func_name')

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
        case = self.get_object(pk)
        serializer = apiTestCaseSerializers(case)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        apicase = self.get_object(pk)
        serializer = apiTestCaseSerializers(apicase, data=request.data)
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
    try:
        url = request.data.get("url")
        params = request.data.get("params")
        params = eval(params) if params != '' else None
        method = request.data.get("method")
        headers = request.data.get("headers")
        headers = eval(headers) if headers != '' else None
        user_id = request.data.get("user_id")
    except Exception:
        return Response({'error': u"参数错误"}, status=status.HTTP_400_BAD_REQUEST)
    if user_id:
        user = ApiTokenUser.objects.get(pk=user_id)
        headers['Authorization'] = user.token_value
    try:
        data = WeHttpClient(url,
                            params=params,
                            headers=headers).result(
            method=dict(REQUEST_METHOD).get(int(method))
        )
        return Response({'data': data}, status=status.HTTP_200_OK)
    except Exception, err:
        return Response({'error': err}, status=status.HTTP_400_BAD_REQUEST)


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
    try:
        base_url = Settings.objects.get(project_id=test_user.project_id, setting_type=0).setting_value
        base_header = Settings.objects.get(project_id=test_user.project_id, setting_type=1).setting_value
        login_uri = Settings.objects.get(project_id=test_user.project_id, setting_type=4).setting_value
        login_base_arg = Settings.objects.get(project_id=test_user.project_id, setting_type=5).setting_value
        login_get_token = Settings.objects.get(project_id=test_user.project_id, setting_type=6).setting_value
    except Settings.DoesNotExist, err:
        return Response({'error': err})
    url = base_url + '/' + login_uri.lstrip("/")
    params = dict(user_arg.items() + eval(login_base_arg).items())
    data = WeHttpClient(url,
                        headers=eval(base_header),
                        params=params).body(method="POST")
    token_path = login_get_token.split('.')
    if data.get('type') == 'json':
        for x in token_path:
            data = data.get('content').get(x)
        ApiTokenUser.objects.filter(pk=int(user_id)).update(token_value= "token " + data)
        return Response({'data': data})
    else:
        return Response({'error': u'更新token失败'})
