# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-05 16:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_auto_20160831_2103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goal',
            name='start',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='step',
            name='start',
            field=models.DateTimeField(),
        ),
    ]