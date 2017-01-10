# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-10 16:28
from __future__ import unicode_literals

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20161225_2132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=30, unique=True, validators=[users.models.username_case_insensitive_unique]),
        ),
    ]
