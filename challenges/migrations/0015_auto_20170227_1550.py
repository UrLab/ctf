# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-27 14:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0014_auto_20170217_2046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attempt',
            name='attempt',
            field=models.CharField(max_length=5000),
        ),
        migrations.AlterField(
            model_name='challenge',
            name='flag',
            field=models.CharField(max_length=5000),
        ),
    ]