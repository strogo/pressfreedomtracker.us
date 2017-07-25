# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-21 21:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('incident', '0013_add_blocks_to_incident_body_and_updates'),
    ]

    operations = [
        migrations.AddField(
            model_name='incidentpage',
            name='display_date_month_only',
            field=models.BooleanField(default=False, help_text='If checked, only the month and year of the incident will be displayed.'),
        ),
    ]