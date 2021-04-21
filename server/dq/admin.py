from django.contrib import admin
from .models import Queue, DownloadJob


class QueueAdmin(admin.ModelAdmin):
    pass


class DownloadJobAdmin(admin.ModelAdmin):
    pass


# Register your models here.
admin.site.register(Queue, QueueAdmin)
admin.site.register(DownloadJob, DownloadJobAdmin)
