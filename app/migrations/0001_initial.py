# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-01 15:45
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('sent', models.DateTimeField(auto_now_add=True)),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipient', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('sent',),
            },
        ),
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('FIVE_DAY_CHALLENGE', 'FIVE_DAY_CHALLENGE'), ('CUSTOM', 'CUSTOM')], max_length=256)),
                ('name', models.TextField(max_length=256)),
                ('description', models.TextField(max_length=1024)),
                ('start', models.DateTimeField()),
                ('active', models.BooleanField(default=False)),
                ('lives', models.IntegerField(default=3)),
                ('complete', models.BooleanField(default=False)),
                ('deleted', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-start',),
            },
        ),
        migrations.CreateModel(
            name='Step',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.TextField(max_length=256)),
                ('description', models.TextField(max_length=1024)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('time_tracked', models.DateTimeField(blank=True, null=True)),
                ('complete', models.BooleanField(default=False)),
                ('comments', models.TextField(blank=True, max_length=1024)),
                ('goal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='steps', to='app.Goal')),
            ],
            options={
                'ordering': ('start',),
            },
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Timezone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='email',
            name='step',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='emails', to='app.Step'),
        ),
    ]
