from django.contrib import admin

from backups.models import BackupJob, BackupTarget

class BackupJobsAdmin(admin.ModelAdmin):
    list_display = ["target", "name"]

class BackupJobsInline(admin.StackedInline):
    model = BackupJob
    extra = 0

@admin.register(BackupTarget)
class BackupTargetAdmin(admin.ModelAdmin):
    list_display  = [
        "hostname",
        "ip",
        "port",
        "client_last_contact",
        "client_version",
        "client_reachable"
    ]

    inlines = [BackupJobsInline]
