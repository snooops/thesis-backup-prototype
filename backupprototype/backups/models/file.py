from django.db import models

# Create your models here.
class BackupFileJob(models.Model):
    
    # give it a name
    name = models.CharField(max_length=2048)

    # reference to the job
    backup_job = models.ForeignKey(
        "BackupJob",
        on_delete=models.CASCADE,
    )


# storing the paths for each entry
class BackupFileJobPath(models.Model):

    backup_file_job = models.ForeignKey(
        "BackupFileJob",
        on_delete=models.CASCADE,
    )

    # hostname of the backup target.
    path = models.CharField(max_length=2048) 