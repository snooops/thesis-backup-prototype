from django.contrib import admin

# Register your models here.
from .models import BackupTarget

class BackupTargetAdmin(admin.ModelAdmin):
    list_display  = [
        "hostname",
        "ip",
        "port",
        "client_last_contact",
        "client_version",
        "client_reachable"
    ]

admin.site.register(BackupTarget, BackupTargetAdmin)