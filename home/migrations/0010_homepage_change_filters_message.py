# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-18 18:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_auto_20170717_2304'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='change_filters_message',
            field=models.CharField(default='Change filters to search the incident database.', help_text='Text for the filter bar when no filters are applied.', max_length=255),
        ),
    ]
