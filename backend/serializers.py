from .models import ApiTestCases, ApiTokenUser
from rest_framework import serializers


class apiTokenUserSerializers(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=62)
    user_desc = serializers.CharField(max_length=200)
    token_api = serializers.CharField(max_length=200)
    token_term = serializers.IntegerField()
    token_value = serializers.CharField(max_length=200, required=False, allow_blank=True)

    class Meta:
        model = ApiTokenUser
        fields = ('id', 'username', 'password','user_desc', 'token_api',
                  'token_value', 'token_term', 'update_time')

    def create(self, validated_data):
        user = ApiTokenUser.objects.create(**validated_data)
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.password = validated_data.get('password', instance.password)
        instance.user_desc = validated_data.get('user_desc', instance.user_desc)
        instance.token_api = validated_data.get('token_api', instance.token_api)
        instance.token_term = validated_data.get('token_term', instance.token_term)
        instance.save()
        return instance

class apiTestCaseSerializers(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50)
    description = serializers.CharField(max_length=200)
    suite_name = serializers.CharField(max_length=50)
    func_name = serializers.CharField(max_length=50)
    method = serializers.IntegerField()
    uri = serializers.CharField(max_length=200)
    is_token = serializers.BooleanField()
    token_user_id = serializers.IntegerField()
    params = serializers.CharField(max_length=500, required=False, allow_blank=True)
    headers = serializers.CharField(max_length=500, required=False, allow_blank=True)
    project_id = serializers.IntegerField()

    class Meta:
        model = ApiTestCases
        fields = ('id', 'name', 'description','suite_name', 'func_name',
                  'method', 'uri', 'is_token', 'token_user_id', 'params',
                  'headers', 'project_id')


    def create(self, validated_data):
        user = ApiTestCases.objects.create(**validated_data)
        return user

    def update(self, instance, validate):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.suite_name = validated_data.get('suite_name', instance.suite_name)
        instance.func_name = validated_data.get('func_name', instance.func_name)
        instance.method = validated_data.get('method', instance.method)
        instance.uri = validated_data.get('uri', instance.uri)
        instance.is_token = validated_data.get('is_token', instance.is_token)
        instance.token_user = validated_data.get('token_user', instance.token_user)
        instance.params = validated_data.get('params', instance.params)
        instance.headers = validated_data.get('headers', instance.headers)
        instance.project_id = validated_data.get('project_id', instance.project_id)
        return instance
