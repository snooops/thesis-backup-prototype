from django.db import models

# Create your models here.
class BackupTarget(models.Model):
    
    # hostname of the backup target.
    hostname = models.CharField(max_length=63)

    # IP Address, can be IPv4 or IPv6.
    ip = models.GenericIPAddressField(protocol='both')

    # Port of the Backup Client Agent.
    port = models.IntegerField()

    # Last ping pong
    client_last_contact = models.DateTimeField(blank=True, null=True)

    # Version of the agent, will be filled after first contact
    client_version = models.CharField(max_length=128, blank=True)

    # error of the client if there is some
    client_error_message = models.TextField(blank=True)

    # outcome of last ping check
    client_reachable = models.BooleanField(default=False)


class BackupJob(models.Model):

    backup_target = models.ForeignKey(
        "BackupTarget",
        on_delete=models.CASCADE,
    )

    name = models.CharField(max_length=128)

    # for cron job syntax
    run_cron =  models.CharField(max_length=128)

    def hostname(self):
        return self.backup_target.hostname
    
    def ip(self):
        return self.backup_target.ip
    
    def __str__(self):
        return self.name