# Generated by Django 5.0.3 on 2024-03-29 13:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backups', '0005_backupjob_backupfilejobs'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='BackupFileJobs',
            new_name='BackupFileJob',
        ),
    ]
