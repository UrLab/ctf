# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-09 17:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0005_auto_20160407_1831'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='resolution',
            unique_together=set([('challenge', 'team')]),
        ),
    ]
