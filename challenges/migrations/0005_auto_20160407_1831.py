# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-07 18:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0004_resolution'),
    ]

    operations = [
        migrations.RenameField(
            model_name='challenge',
            old_name='decription',
            new_name='description',
        ),
    ]
