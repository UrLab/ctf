# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-18 18:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0011_auto_20170110_1728'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challenge',
            name='phase',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='challenges.Phase'),
        ),
    ]
