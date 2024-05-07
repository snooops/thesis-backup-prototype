# Create your tasks here
from backups.models import BackupTarget, BackupJob, BackupFileJob
from celery import shared_task
import requests
from django.utils import timezone
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from celery.schedules import crontab


def schedule_backup_jobs():
    """Ping all the backup targets and check if they are reachable."""
    backup_file_jobs = BackupFileJob.objects.all()
    for backup_file_job in backup_file_jobs:
        # get the backup_job attributes
        backup_job = backup_file_job.backup_job

        # get backup target host attributes
        backup_target = backup_job.backup_target

        new_periodic_task = PeriodicTask(
            name=f"{backup_target.hostname} at {backup_job.name}",
            task="backups.tasks.file.run_backup",
        )

        # saving entry
        new_periodic_task.save()


def run_file_backup():
    print("Do the filebackup")
