# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-12 22:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0010_add_custom_embed_block'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('label', models.CharField(max_length=255)),
                ('data_point', models.CharField(max_length=255)),
                ('params', models.CharField(blank=True, help_text='Whitespace-separated list of arguments to be passed to the data point function', max_length=255, null=True)),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='data_items', to='common.CategoryPage')),
            ],
            options={
                'abstract': False,
                'ordering': ['sort_order'],
            },
        ),
    ]
