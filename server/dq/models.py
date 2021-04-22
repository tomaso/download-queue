from django.db import models


class Queue(models.Model):
    name = models.CharField(max_length=64)
    paused = models.BooleanField(default=False)


class DownloadJob(models.Model):
    target_directory = models.CharField(max_length=256)
    url = models.CharField(max_length=1024)
    queue = models.ForeignKey(Queue, on_delete=models.CASCADE, blank=True, null=True)
    completed = models.BooleanField(default=False)
    priority = models.DecimalField(max_digits=10, decimal_places=0)
#    progress
#    start_time
#    end_time
