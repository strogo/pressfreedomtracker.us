# Generated by Django 2.2.12 on 2020-06-10 19:01

import common.blocks
from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.embeds.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('incident', '0051_topicpage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topicpage',
            name='content',
            field=wagtail.core.fields.StreamField([('heading_2', wagtail.core.blocks.StructBlock([('content', wagtail.core.blocks.CharBlock())])), ('raw_html', wagtail.core.blocks.RawHTMLBlock()), ('rich_text', wagtail.core.blocks.RichTextBlock()), ('tweet', wagtail.core.blocks.StructBlock([('tweet', wagtail.embeds.blocks.EmbedBlock())]))], blank=True),
        ),
        migrations.AlterField(
            model_name='topicpage',
            name='sidebar',
            field=wagtail.core.fields.StreamField([('heading_2', wagtail.core.blocks.StructBlock([('content', wagtail.core.blocks.CharBlock())])), ('rich_text', common.blocks.RichTextTemplateBlock(features=['bold', 'italic', 'link', 'ol', 'ul'], icon='doc-full', label='Rich Text')), ('tweet', wagtail.core.blocks.StructBlock([('tweet', wagtail.embeds.blocks.EmbedBlock())])), ('stat_table', common.blocks.StatTableBlock()), ('button', wagtail.core.blocks.StructBlock([('text', wagtail.core.blocks.TextBlock(required=True)), ('url', wagtail.core.blocks.URLBlock(required=True))]))], blank=True),
        ),
    ]
