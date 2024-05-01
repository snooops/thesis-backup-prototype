# Create your tasks here
from backups.models import BackupTarget, BackupJob, BackupFileJob

from celery import shared_task
import requests
from django.utils import timezone
from django_celery_beat.models import PeriodicTask, CrontabSchedule

# -- Inside the function you want to add task dynamically 

schedule = CrontabSchedule.objects.create(minute='*/1')
PeriodicTask.objects.create(name='adder',
                                   task='apps.task.add', crontab=schedule)


@shared_task
def schedule_backup_jobs():
    """Ping all the backup targets and check if they are reachable.
    """
    backup_file_jobs = BackupFileJob.objects.all()
    for backup_file_job in backup_file_jobs:
        # get the backup_job attributes
        backup_job = backup_file_job.backup_job

        # get backup target host attributes
        backup_target = backup_job.backup_target
        
        # if the backup target is not reachable continue
        if not backup_target.client_reachable:
            continue