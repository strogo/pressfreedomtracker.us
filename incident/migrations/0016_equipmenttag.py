# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-05 21:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('incident', '0015_auto_20170505_2154'),
    ]

    operations = [
        migrations.CreateModel(
            name='EquipmentTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('category', models.CharField(choices=[('SEIZED', 'seized'), ('BROKEN', 'broken')], default='SEIZED', max_length=255)),
                ('incident', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='equipment', to='incident.IncidentPage')),
            ],
        ),
    ]