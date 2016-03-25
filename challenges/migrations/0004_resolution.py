# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-25 19:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '__first__'),
        ('challenges', '0003_challenge_flag'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resolution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now=True)),
                ('challenge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='challenges.Challenge')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Team')),
            ],
        ),
    ]
