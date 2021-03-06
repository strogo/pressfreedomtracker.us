# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-19 18:06
from __future__ import unicode_literals

from django.db import migrations


def create_general_filters(apps, schema_migration):
    Site = apps.get_model('wagtailcore.Site')
    IncidentFilterSettings = apps.get_model('common.IncidentFilterSettings')
    GeneralIncidentFilter = apps.get_model('common.GeneralIncidentFilter')

    site = Site.objects.get(is_default_site=True)
    settings, _ = IncidentFilterSettings.objects.get_or_create(site=site)

    GeneralIncidentFilter.objects.bulk_create([
        GeneralIncidentFilter(
            incident_filter_settings=settings,
            incident_filter=incident_filter,
            sort_order=index,
        )
        for index, incident_filter in enumerate([
            'date',
            'affiliation',
            'city',
            'state',
            'targets',
            'tags',
            'lawsuit_name',
            'venue',
        ])
    ])


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0050_auto_20180319_1805'),
    ]

    operations = [
        migrations.RunPython(create_general_filters, migrations.RunPython.noop, elidable=True),
    ]
