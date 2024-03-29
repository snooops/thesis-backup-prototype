# Generated by Django 5.0.3 on 2024-03-24 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backups', '0003_alter_backuptarget_client_last_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='backuptarget',
            name='client_error_message',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='backuptarget',
            name='client_reachable',
            field=models.BooleanField(default=False),
        ),
    ]
