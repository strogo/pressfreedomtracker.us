# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-27 22:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incident', '0005_merge_20170626_2248'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='incidentpage',
            name='state',
        ),
    ]