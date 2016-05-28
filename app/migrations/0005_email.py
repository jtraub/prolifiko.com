# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-21 11:33
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20160515_1913'),
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name='ID')),
                ('name', models.TextField()),
                ('user_journey_ref', models.TextField()),
                ('content', wagtail.wagtailcore.fields.RichTextField()),
                ('subject', models.TextField()),
            ],
        ),
    ]