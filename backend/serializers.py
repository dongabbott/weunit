from .models import ApiTestCases, ApiTokenUser, TestSuite, SuiteChangeLog
from rest_framework import serializers


class apiTokenUserSerializers(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=62)
    user_desc = serializers.CharField(max_length=200)
    project_id = serializers.IntegerField()
    token_term = serializers.IntegerField()
    token_value = serializers.CharField(max_length=200, required=False, allow_blank=True)

    class Meta:
        model = ApiTokenUser
        fields = ('id', 'username', 'password', 'user_desc', 'project_id',
                  'token_value', 'token_term', 'update_time')

    def create(self, validated_data):
        user = ApiTokenUser.objects.create(**validated_data)
        return user

    def update(self, instance, validated_data):
        instance.project_id = validated_data.get('project_id', instance.project_id)
        instance.username = validated_data.get('username', instance.username)
        instance.password = validated_data.get('password', instance.password)
        instance.user_desc = validated_data.get('user_desc', instance.user_desc)
        instance.token_term = validated_data.get('token_term', instance.token_term)
        instance.save()
        return instance

class SuiteChangeLogSerializers(serializers.ModelSerializer):

    class Meta:
        model = SuiteChangeLog
        fields = ('id', 'code_content', 'create_time')

class testSuiteSerializers(serializers.ModelSerializer):
    suite_name = serializers.CharField(max_length=50)
    suite_desc = serializers.CharField(max_length=200)
    project_id = serializers.IntegerField()
    case_count = serializers.SerializerMethodField(source='')
    suite_log = SuiteChangeLogSerializers(many=True, read_only=True)

    class Meta:
        model = TestSuite
        fields = ('id', 'suite_name', 'suite_desc', 'project_id', 'create_time', 'suite_log', 'case_count')

    def get_case_count(self, obj):
        return ApiTestCases.objects.filter(suite_id=obj.id).count()

    def create(self, validated_data):
        suite = TestSuite.objects.create(**validated_data)
        return suite


class apiTestCaseSerializers(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50)
    description = serializers.CharField(max_length=200)
    func_name = serializers.CharField(max_length=50)
    method = serializers.IntegerField()
    uri = serializers.CharField(max_length=200)
    is_token = serializers.BooleanField()
    params = serializers.CharField(max_length=500, required=False, allow_blank=True)
    headers = serializers.CharField(max_length=500, required=False, allow_blank=True)
    project_id = serializers.IntegerField()
    suite_id = serializers.IntegerField()
    token_user_id = serializers.IntegerField(required=False)

    class Meta:
        model = ApiTestCases
        fields = ('id', 'name', 'description','suite_id', 'func_name',
                  'method', 'uri', 'is_token', 'params', 'token_user_id',
                  'headers', 'project_id', 'create_time')

    def create(self, validated_data):
        case = ApiTestCases.objects.create(**validated_data)
        return case

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.func_name = validated_data.get('func_name', instance.func_name)
        instance.method = validated_data.get('method', instance.method)
        instance.uri = validated_data.get('uri', instance.uri)
        instance.is_token = validated_data.get('is_token', instance.is_token)
        instance.params = validated_data.get('params', instance.params)
        instance.headers = validated_data.get('headers', instance.headers)
        instance.project_id = validated_data.get('project_id', instance.project_id)
        instance.suite_id = validated_data.get('suite_id', instance.suite_id)
        instance.token_user_id = validated_data.get('token_user_id', instance.token_user_id)
        instance.save()
        return instance
