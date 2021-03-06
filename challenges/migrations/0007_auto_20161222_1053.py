# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-12-22 10:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0006_auto_20160409_1736'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'categories'},
        ),
        migrations.AddField(
            model_name='hint',
            name='visible',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='challenge',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
