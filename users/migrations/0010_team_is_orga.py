# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-18 18:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20170110_1728'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='is_orga',
            field=models.BooleanField(default=False),
        ),
    ]
