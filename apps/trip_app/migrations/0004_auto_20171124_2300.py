# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-11-24 23:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('trip_app', '0003_auto_20171124_2239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='travel_from',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='trip',
            name='travel_to',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
