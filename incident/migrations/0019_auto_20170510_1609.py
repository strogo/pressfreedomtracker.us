# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-10 16:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('incident', '0018_auto_20170508_1659'),
    ]

    operations = [
        migrations.CreateModel(
            name='TargetsTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='incidentpage',
            name='targets',
        ),
        migrations.AddField(
            model_name='targetstag',
            name='content_object',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='tagged_targets', to='incident.IncidentPage'),
        ),
        migrations.AddField(
            model_name='targetstag',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='incident_targetstag_items', to='taggit.Tag'),
        ),
    ]