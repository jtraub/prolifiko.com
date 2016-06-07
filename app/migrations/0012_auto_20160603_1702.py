# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-03 17:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_email_step'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='step',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='emails',
                to='app.Step'),
        ),
    ]