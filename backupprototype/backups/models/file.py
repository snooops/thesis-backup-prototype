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

    # fs type of the path, file or directory?
    fs_type = models.CharField(max_length=16)

    # last time the file was modified
    stat_modified = models.IntegerField()

    # last time the permissions of the file where changed
    stat_changed = models.IntegerField()

    stat_size = models.IntegerField()