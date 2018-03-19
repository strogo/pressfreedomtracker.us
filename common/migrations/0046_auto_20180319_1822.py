# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-19 18:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0045_auto_20180312_1932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoryincidentfilter',
            name='incident_filter',
            field=models.CharField(choices=[('actor', 'Actor'), ('arrest_status', 'Arrest status'), ('assailant', 'Assailant'), ('border_point', 'Border point'), ('charged_under_espionage_act', 'Charged under espionage act?'), ('charges', None), ('current_charges', 'Current Charges'), ('denial_of_entry', 'Denied entry?'), ('detention_date', 'Detention date'), ('detention_status', 'Detention status'), ('did_authorities_ask_about_work', "Did authorities ask intrusive questions about journalist's work?"), ('did_authorities_ask_for_device_access', 'Did authorities ask for device access?'), ('did_authorities_ask_for_social_media_pass', 'Did authorities ask for social media password?'), ('did_authorities_ask_for_social_media_user', 'Did authorities ask for social media username?'), ('dropped_charges', 'Dropped Charges'), ('equipment_broken', 'Equipment Broken'), ('equipment_seized', 'Equipment Seized'), ('held_in_contempt', 'If subject refused to cooperate, were they held in contempt?'), ('is_search_warrant_obtained', 'Search warrant obtained?'), ('legal_order_type', 'Legal order type'), ('links', 'incident page links'), ('politicians_or_public_figures_involved', 'Politicians or public officials involved'), ('release_date', 'Release date'), ('status_of_charges', 'Status of charges'), ('status_of_prior_restraint', 'Status of prior restraint'), ('status_of_seized_equipment', 'Status of seized equipment'), ('stopped_at_border', 'Stopped at border?'), ('stopped_previously', 'Stopped previously?'), ('subpoena_status', 'Subpoena status'), ('subpoena_type', 'Subpoena type'), ('target_nationality', 'Target Nationality'), ('target_us_citizenship_status', 'US Citizenship Status'), ('targets_whose_communications_were_obtained', 'Journalists/Organizations whose communications were obtained in leak investigation'), ('third_party_business', 'Third party business'), ('third_party_in_possession_of_communications', 'Third party in possession of communications'), ('unnecessary_use_of_force', 'Unnecessary use of force?'), ('was_journalist_targeted', 'Was journalist targeted?'), ('were_devices_searched_or_seized', 'Were devices searched or seized?')], max_length=255),
        ),
    ]
