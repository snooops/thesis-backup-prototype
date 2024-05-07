# thesis-backup-prototype
Prototype of a backup solution for my bachelor thesis


# Requirements
* rabbitmq-server >= 3.10

# Not tested yet
* symbolic links


# Next Steps
* do this: django-celery-beat
    https://stackoverflow.com/questions/37339649/how-to-dynamically-add-a-scheduled-task-to-celery-beat

Start a celery worker
`celery -A backupprototype worker --loglevel=info`

Start the celery beat
`celery -A backupprototype beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler`

