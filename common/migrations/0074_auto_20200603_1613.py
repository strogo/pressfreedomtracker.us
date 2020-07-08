# Generated by Django 2.2.12 on 2020-06-03 16:13

import common.validators
from django.db import migrations, models
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0073_sitesettings_incident_sidebar_note'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='banner_content',
            field=wagtail.core.fields.RichTextField(blank=True, help_text='If set an alert banner will appear on the site with this message', null=True, validators=[common.validators.TemplateValidator()], verbose_name='Banner Content'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='homepage_only',
            field=models.BooleanField(default=True, help_text='Show banner <em>only</em> on homepage (if not set, will show sitewide)', verbose_name='Homepage Only'),
        ),
    ]