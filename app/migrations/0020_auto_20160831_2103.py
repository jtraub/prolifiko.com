# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-31 20:03
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_goal_deleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='goal',
            name='timezone',
            field=models.TextField(default='Europe/London'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='goal',
            name='start',
            field=models.DateTimeField(default=datetime.datetime.utcnow),
        ),
        migrations.AlterField(
            model_name='step',
            name='start',
            field=models.DateTimeField(default=datetime.datetime.utcnow),
        ),
    ]