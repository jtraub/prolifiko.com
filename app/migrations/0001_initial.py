# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-10 08:05
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=144)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Step',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=144)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('complete', models.BooleanField()),
                ('comments', models.TextField(max_length=144)),
                ('goal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Goal')),
            ],
        ),
    ]
