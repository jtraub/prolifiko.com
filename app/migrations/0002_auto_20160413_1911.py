# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-13 19:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='step',
            name='comments',
            field=models.TextField(blank=True, max_length=144),
        ),
        migrations.AlterField(
            model_name='step',
            name='complete',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='step',
            name='start',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
