# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-31 08:39
from __future__ import unicode_literals

from datetime import datetime
from django.conf import settings
from django.db import migrations, models
from django.db.models import deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0008_goal_complete'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='email',
            name='content',
        ),
        migrations.RemoveField(
            model_name='email',
            name='subject',
        ),
        migrations.RemoveField(
            model_name='email',
            name='user_journey_ref',
        ),
        migrations.AddField(
            model_name='email',
            name='sent',
            field=models.DateTimeField(
                auto_now_add=True,
                default=datetime(2016, 5, 31, 8, 37, 35, 304920, tzinfo=utc)
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='email',
            name='user',
            field=models.ForeignKey(default=None,
                                    on_delete=deletion.CASCADE,
                                    related_name='recipient',
                                    to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
