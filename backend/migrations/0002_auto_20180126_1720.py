# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-01-26 09:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apitestcases',
            name='suite_name',
        ),
        migrations.AddField(
            model_name='apitestcases',
            name='suite',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.TestSuite'),
        ),
    ]
