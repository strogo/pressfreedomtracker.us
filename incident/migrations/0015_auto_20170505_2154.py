# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-05 21:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incident', '0014_auto_20170505_2052'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='equipmenttag',
            name='content_object',
        ),
        migrations.RemoveField(
            model_name='equipmenttag',
            name='tag',
        ),
        migrations.RemoveField(
            model_name='incidentpage',
            name='equipment_seized',
        ),
        migrations.DeleteModel(
            name='EquipmentTag',
        ),
    ]