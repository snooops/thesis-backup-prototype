from django.contrib import admin
from backups.models import BackupFileJob, BackupJob, BackupFileJobPath

class BackupFilePathsInline(admin.StackedInline):
    model = BackupFileJobPath
    extra = 1


@admin.register(BackupFileJob)
class FileBackupAdmin(admin.ModelAdmin):

    # Overview page
    list_display = ('backup_target', 'name', 'backup_job_name')

    def backup_job_name(self, instance):
        return instance.backup_job.name

    def backup_target(self, instance):
        return self.backup_target_name(instance.backup_job.backup_target)
    
    def backup_target_name(self, instance):
        return instance.hostname

         
    # Single entry page
    inlines = [BackupFilePathsInline]
    