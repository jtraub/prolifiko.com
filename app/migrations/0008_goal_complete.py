# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-28 10:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_goal_lives'),
    ]

    operations = [
        migrations.AddField(
            model_name='goal',
            name='complete',
            field=models.BooleanField(default=False),
        ),
    ]
