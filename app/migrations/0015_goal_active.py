# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-26 18:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_remove_goal_end'),
    ]

    operations = [
        migrations.AddField(
            model_name='goal',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]
