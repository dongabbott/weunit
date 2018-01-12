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
from  django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination


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
