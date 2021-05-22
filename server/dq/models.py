from django.db import models


class Queue(models.Model):
    name = models.CharField(max_length=64)
    paused = models.BooleanField(default=False)


class DownloadJob(models.Model):
    target_directory = models.CharField(max_length=256)
    target_file = models.CharField(max_length=256, default="file")
    url = models.CharField(max_length=1024)
    queue = models.ForeignKey(Queue, on_delete=models.CASCADE, blank=True, null=True)
    completed = models.BooleanField(default=False)
    priority = models.DecimalField(max_digits=10, decimal_places=0)
    progress = models.DecimalField(max_digits=3, decimal_places=0, default=0)
#    start_time
#    end_time
