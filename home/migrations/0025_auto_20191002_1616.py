# Generated by Django 2.1.11 on 2019-10-02 16:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0024_auto_20191002_1605'),
    ]

    operations = [
        migrations.RenameField(
            model_name='homepagefeature',
            old_name='incident',
            new_name='page',
        ),
    ]
