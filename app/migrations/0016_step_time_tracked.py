# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-26 18:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_goal_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='step',
            name='time_tracked',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]