# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-02 09:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0026_auto_20170802_0938'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialsharingseosettings',
            name='twitter',
            field=models.CharField(blank=True, help_text='Your Twitter username', max_length=255, null=True),
        ),
    ]
