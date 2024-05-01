# Create your tasks here
from backups.models import BackupTarget

from celery import shared_task
import requests
from django.utils import timezone


@shared_task
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