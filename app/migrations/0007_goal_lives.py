# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-24 08:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_load_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='goal',
            name='lives',
            field=models.IntegerField(default=3),
        ),
    ]
