# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-17 21:10
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ctf', '0002_iplog_date'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='iplog',
            unique_together=set([('ip', 'user')]),
        ),
    ]