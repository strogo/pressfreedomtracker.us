# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-21 18:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('incident', '0030_target_kind'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incidentpage',
            name='status_of_prior_restraint',
            field=models.CharField(blank=True, choices=[('PENDING', 'pending'), ('DROPPED', 'dropped'), ('STRUCK_DOWN', 'struck down'), ('UPHELD', 'upheld'), ('IGNORED', 'ignored')], max_length=255, null=True, verbose_name='Status of prior restraint'),
        ),
        migrations.AlterField(
            model_name='incidentpage',
            name='subpoena_status',
            field=models.CharField(blank=True, choices=[('PENDING', 'pending'), ('DROPPED', 'dropped'), ('QUASHED', 'quashed'), ('UPHELD', 'upheld'), ('CARRIED_OUT', 'carried out'), ('IGNORED', 'ignored')], max_length=255, null=True, verbose_name='Subpoena status'),
        ),
    ]
