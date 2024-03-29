# Generated by Django 5.0.3 on 2024-03-24 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BackupTarget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostname', models.CharField(max_length=63)),
                ('ip', models.GenericIPAddressField()),
                ('port', models.IntegerField()),
                ('client_last_contact', models.DateTimeField()),
                ('client_version', models.CharField(max_length=128)),
            ],
        ),
    ]
