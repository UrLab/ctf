# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-12-23 18:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20161223_1733'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='secret_key',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='name',
            field=models.CharField(max_length=30),
        ),
    ]