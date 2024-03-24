# Source code from: https://github.com/jcass77/django-apscheduler/README.md
# runapscheduler.py 
import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util
from backups.models import BackupTarget
from django.utils import timezone
#from datetime import datetime
import requests
logger = logging.getLogger(__name__)


def ping_targets():
    """Ping all the backup targets and check if they are reachable.
    """
    backups_targets = BackupTarget.objects.all()

    for backup_target in backups_targets:
        try:
            # building url 
            url = f'http://{backup_target.ip}:{backup_target.port}'
            target_response = requests.get(f'{url}/ping', timeout=20)
            target_response.raise_for_status()
            
            # parsing response json into a python dict
            client_answer = target_response.json()
            
            # saving values
            backup_target.client_version = client_answer["version"]
            backup_target.client_error_message = client_answer["message"]
            backup_target.client_last_contact = timezone.now()
            backup_target.client_reachable = True
            backup_target.save(update_fields=['client_version','client_last_contact', 'client_reachable', 'client_error_message'])

        except requests.Timeout as err:
            backup_target.client_error_message = f"Timeout: {err}"
            backup_target.client_reachable = False
            backup_target.save(update_fields=['client_error_message', 'client_reachable'])

        except Exception as err:
            backup_target.client_error_message = f"Some unhandled Exception: {err}"
            backup_target.client_reachable = False
            backup_target.save(update_fields=['client_error_message', 'client_reachable'])
    pass


# The `close_old_connections` decorator ensures that database connections, that have become
# unusable or are obsolete, are closed before and after your job has run. You should use it
# to wrap any jobs that you schedule that access the Django database in any way. 
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age` from the database.
    It helps to prevent the database from filling up with old historical records that are no
    longer useful.
    
    :param max_age: The maximum length of time to retain historical job execution records.
                    Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            ping_targets,
            trigger=CronTrigger(second="*/30"),  # Every 10 seconds
            id="ping_targets",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
            day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
