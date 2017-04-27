# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-04-24 15:17
from __future__ import unicode_literals

from django.db import migrations
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('incident', '0010_incidentcategorization'),
        ('home', '0004_auto_20170424_1504'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='incident_index_page',
            field=modelcluster.fields.ParentalKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='homepage', to='incident.IncidentIndexPage'),
        ),
    ]
