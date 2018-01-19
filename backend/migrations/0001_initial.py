# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-01-18 11:21
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApiTestCases',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='\u7528\u4f8b\u540d\u79f0')),
                ('description', models.TextField(verbose_name='\u63cf\u8ff0')),
                ('suite_name', models.CharField(max_length=30, verbose_name='unittest\u5957\u4ef6\u540d')),
                ('func_name', models.CharField(max_length=30, verbose_name='unittest\u65b9\u6cd5\u540d')),
                ('method', models.IntegerField(choices=[(1, b'GET'), (2, b'POST'), (3, b'PUT'), (4, b'DELETE')], verbose_name='\u8bf7\u6c42\u65b9\u6cd5')),
                ('uri', models.CharField(max_length=100, verbose_name='\u8bf7\u6c42\u5730\u5740')),
                ('is_token', models.BooleanField(verbose_name='\u662f\u5426\u9700\u8981token')),
                ('params', models.CharField(max_length=500, verbose_name='\u8bf7\u6c42\u4f53')),
                ('headers', models.CharField(default={b'Accept': b'application/vnd.timehut.v5+json', b'Content-Type': b'application/x-www-form-urlencoded; charset=UTF-8', b'User-Agent': b'com.liveyap.timehut/5.1.1.2 (android 7.1.1, OD105) (SOURCE/aliyun, VERSION_CODE/227)'}, max_length=500, verbose_name='\u8bf7\u6c42\u5934')),
                ('create_time', models.DateTimeField(auto_now=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_time', models.DateField(auto_now_add=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='project.Projects')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'apicase',
            },
        ),
        migrations.CreateModel(
            name='ApiTokenUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32, verbose_name='\u7528\u6237\u540d')),
                ('password', models.CharField(max_length=50, verbose_name='\u5bc6\u7801')),
                ('user_desc', models.CharField(max_length=200, verbose_name='\u7528\u6237\u63cf\u8ff0')),
                ('token_value', models.CharField(max_length=200, verbose_name='token\u503c')),
                ('token_term', models.BigIntegerField(verbose_name='token\u6709\u6548\u671f')),
                ('create_time', models.DateField(auto_now=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_time', models.DateField(auto_now_add=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='project.Projects')),
            ],
            options={
                'db_table': 'testuser',
            },
        ),
        migrations.CreateModel(
            name='TestApiUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_time', models.DateField(auto_now_add=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.ApiTestCases')),
                ('token_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.ApiTokenUser')),
            ],
            options={
                'db_table': 'apiuser',
            },
        ),
    ]
