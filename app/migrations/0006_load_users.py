# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-21 11:37
from __future__ import unicode_literals

from os.path import abspath, join, dirname
from django.db import migrations
from django.core.management import call_command


def load_fixture(apps, schema_editor):
    call_command('loaddata', abspath(
        join(dirname(__file__), '../fixtures', 'users.json')))


def unload_fixture(apps, schema_editor):
    User = apps.get_model("auth", "User")
    User.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_email'),
    ]

    operations = [
        migrations.RunPython(load_fixture, reverse_code=unload_fixture),
    ]
