# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.response import Response
from .models import Projects, Settings, Tasks
from .serializers import ProjectSerializer
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics
from rest_framework import filters
from backend.utils.options import REQUEST_METHOD, SETTING_CLASS


class ProjectList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    queryset = Projects.objects.all()
    serializer_class = ProjectSerializer
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('project_name', 'project_desc')

    def list(self, request, *args, **kwargs):
        response = super(ProjectList, self).list(request, args, kwargs)
        response.data['setting_type'] = [{"key":key , "name": name} for (key, name) in SETTING_CLASS]
        response.data['reqeust_method'] = [{"key":key , "name": name} for (key, name) in REQUEST_METHOD]
        return response

    def post(self, request, format=None):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_id=request.user.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectDetail(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get_object(self, pk):
        try:
            return Projects.objects.get(pk=pk)
        except Projects.DoesNotExist:
            raise Http404

    def filter_request(self, request):
        settings = request.data.get('setting')
        if settings:
            for s in settings:
                if s['setting_type'] == '' and s['value'] == '':
                    settings.remove(s)
        request.data['setting'] = settings
        return request.data

    def get(self, request, pk, format=None):
        project = self.get_object(pk)
        serializer = ProjectSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        project = self.get_object(pk)
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save(user_id=request.user.id)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        project = self.get_object(pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SettingDetail(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get_setting(self, pk):
        try:
            return Settings.objects.get(pk=pk)
        except Settings.DoesNotExist:
            raise Http404

    def delete(self, request, pk, format=None):
        setting = self.get_setting(pk)
        setting.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def xunit_init(request):
    project_key = request.data.get('project_key')
    try:
        project = Projects.objects.get(project_key=project_key)
    except Projects.DoesNotExist:
        return Response({'detail': u'项目不存在'}, status=status.HTTP_400_BAD_REQUEST)
    task = Tasks.objects.create(project_id=project.id)
    task.save()
    project_data = ProjectSerializer(project)
    return Response({'task_id':task.task_id, 'project':project_data.data})
