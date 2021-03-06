# Generated by Django 2.2.9 on 2020-02-11 21:46

from django.db import migrations


def copy_targets(apps, schema_editor):
    """Copy Leak-Case incident Target data into government workers table"""

    IncidentPage = apps.get_model('incident', 'IncidentPage')
    GovernmentWorker = apps.get_model('incident', 'GovernmentWorker')

    for incident in IncidentPage.objects.all():
        for target in incident.targets_whose_communications_were_obtained.all():
            worker, _ = GovernmentWorker.objects.get_or_create(title=target.title)
            worker.incidents.add(incident)
            worker.save()


class Migration(migrations.Migration):

    dependencies = [
        ('incident', '0041_governmentworker'),
    ]

    operations = [
        migrations.RunPython(
            copy_targets,
            reverse_code=migrations.RunPython.noop,
            elidable=True,
        ),
    ]
