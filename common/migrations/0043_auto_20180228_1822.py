# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-28 18:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0042_create_initial_category_fields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoryincidentfilter',
            name='incident_filter',
            field=models.CharField(choices=[('release_date', 'Release date'), ('targets_whose_communications_were_obtained', 'Journalists/Organizations whose communications were obtained in leak investigation'), ('is_search_warrant_obtained', 'Search warrant obtained?'), ('status_of_seized_equipment', 'Status of seized equipment'), ('current_charges', 'Current Charges'), ('detention_date', 'Detention date'), ('status_of_charges', 'Status of charges'), ('did_authorities_ask_for_social_media_pass', 'Did authorities ask for social media password?'), ('dropped_charges', 'Dropped Charges'), ('assailant', 'Assailant'), ('politicians_or_public_figures_involved', 'Politicians or public officials involved'), ('charged_under_espionage_act', 'Charged under espionage act?'), ('subpoena_status', 'Subpoena status'), ('third_party_in_possession_of_communications', 'Third party in possession of communications'), ('did_authorities_ask_about_work', "Did authorities ask intrusive questions about journalist's work?"), ('stopped_at_border', 'Stopped at border?'), ('status_of_prior_restraint', 'Status of prior restraint'), ('equipment_broken', 'Equipment Broken'), ('unnecessary_use_of_force', 'Unnecessary use of force?'), ('did_authorities_ask_for_social_media_user', 'Did authorities ask for social media username?'), ('actor', 'Actor'), ('arrest_status', 'Arrest status'), ('target_us_citizenship_status', 'US Citizenship Status'), ('held_in_contempt', 'If subject refused to cooperate, were they held in contempt?'), ('were_devices_searched_or_seized', 'Were devices searched or seized?'), ('links', 'incident page links'), ('target_nationality', 'Target Nationality'), ('subpoena_type', 'Subpoena type'), ('was_journalist_targeted', 'Was journalist targeted?'), ('charges', None), ('border_point', 'Border point'), ('third_party_business', 'Third party business'), ('equipment_seized', 'Equipment Seized'), ('detention_status', 'Detention status'), ('stopped_previously', 'Stopped previously?'), ('did_authorities_ask_for_device_access', 'Did authorities ask for device access?'), ('denial_of_entry', 'Denied entry?'), ('legal_order_type', 'Legal order type')], max_length=255),
        ),
    ]