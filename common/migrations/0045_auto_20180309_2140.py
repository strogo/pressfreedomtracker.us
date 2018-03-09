# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-09 21:40
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0044_auto_20180302_1816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoryincidentfilter',
            name='incident_filter',
            field=models.CharField(choices=[('unnecessary_use_of_force', 'Unnecessary use of force?'), ('legal_order_type', 'Legal order type'), ('was_journalist_targeted', 'Was journalist targeted?'), ('links', 'incident page links'), ('did_authorities_ask_for_social_media_user', 'Did authorities ask for social media username?'), ('detention_date', 'Detention date'), ('did_authorities_ask_for_device_access', 'Did authorities ask for device access?'), ('denial_of_entry', 'Denied entry?'), ('held_in_contempt', 'If subject refused to cooperate, were they held in contempt?'), ('is_search_warrant_obtained', 'Search warrant obtained?'), ('charged_under_espionage_act', 'Charged under espionage act?'), ('equipment_broken', 'Equipment Broken'), ('status_of_charges', 'Status of charges'), ('status_of_seized_equipment', 'Status of seized equipment'), ('third_party_business', 'Third party business'), ('target_us_citizenship_status', 'US Citizenship Status'), ('did_authorities_ask_about_work', "Did authorities ask intrusive questions about journalist's work?"), ('arrest_status', 'Arrest status'), ('assailant', 'Assailant'), ('did_authorities_ask_for_social_media_pass', 'Did authorities ask for social media password?'), ('actor', 'Actor'), ('equipment_seized', 'Equipment Seized'), ('charges', None), ('dropped_charges', 'Dropped Charges'), ('current_charges', 'Current Charges'), ('subpoena_status', 'Subpoena status'), ('detention_status', 'Detention status'), ('release_date', 'Release date'), ('stopped_at_border', 'Stopped at border?'), ('targets_whose_communications_were_obtained', 'Journalists/Organizations whose communications were obtained in leak investigation'), ('were_devices_searched_or_seized', 'Were devices searched or seized?'), ('status_of_prior_restraint', 'Status of prior restraint'), ('stopped_previously', 'Stopped previously?'), ('subpoena_type', 'Subpoena type'), ('target_nationality', 'Target Nationality'), ('third_party_in_possession_of_communications', 'Third party in possession of communications'), ('border_point', 'Border point'), ('politicians_or_public_figures_involved', 'Politicians or public officials involved')], max_length=255),
        ),
        migrations.AlterField(
            model_name='simplepage',
            name='sidebar_content',
            field=wagtail.wagtailcore.fields.StreamField((('heading', wagtail.wagtailcore.blocks.StructBlock((('content', wagtail.wagtailcore.blocks.CharBlock()),))), ('rich_text', wagtail.wagtailcore.blocks.RichTextBlock())), blank=True, default=None, null=True),
        ),
    ]
