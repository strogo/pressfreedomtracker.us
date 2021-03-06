# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-12 19:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incident', '0027_set_order_to_none'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='charge',
            options={'ordering': ['title']},
        ),
        migrations.AlterModelOptions(
            name='nationality',
            options={'ordering': ['title'], 'verbose_name_plural': 'nationalities'},
        ),
        migrations.AlterModelOptions(
            name='politicianorpublic',
            options={'ordering': ['title'], 'verbose_name': 'Politician or public figure', 'verbose_name_plural': 'politicians or public figures'},
        ),
        migrations.AlterModelOptions(
            name='target',
            options={'ordering': ['title']},
        ),
        migrations.AlterModelOptions(
            name='venue',
            options={'ordering': ['title']},
        ),
    ]
