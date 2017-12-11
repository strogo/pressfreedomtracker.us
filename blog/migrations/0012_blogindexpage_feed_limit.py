# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-07 22:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_blogindexpage_about_blog_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogindexpage',
            name='feed_limit',
            field=models.PositiveIntegerField(default=20, help_text='Maximum number of posts to be included in the syndication feed. 0 for unlimited.'),
        ),
    ]