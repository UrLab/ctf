# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-17 19:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0013_merge_20170130_1307'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('text', models.TextField(default='')),
                ('mini_logo', models.FileField(blank=True, null=True, upload_to='logos/')),
                ('logo', models.FileField(blank=True, null=True, upload_to='logos/')),
            ],
        ),
        migrations.AddField(
            model_name='challenge',
            name='sponsor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='challenges.Sponsor'),
        ),
    ]
