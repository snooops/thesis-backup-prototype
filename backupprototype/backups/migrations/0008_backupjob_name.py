# Generated by Django 5.0.3 on 2024-03-29 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backups', '0007_backupjob_run_cron'),
    ]

    operations = [
        migrations.AddField(
            model_name='backupjob',
            name='name',
            field=models.CharField(default='Run every minute', max_length=128),
            preserve_default=False,
        ),
    ]
