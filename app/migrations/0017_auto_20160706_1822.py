# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-06 18:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_step_time_tracked'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goal',
            name='text',
            field=models.TextField(max_length=1024),
        ),
        migrations.AlterField(
            model_name='step',
            name='comments',
            field=models.TextField(blank=True, max_length=1024),
        ),
        migrations.AlterField(
            model_name='step',
            name='text',
            field=models.CharField(max_length=1024),
        ),
    ]
