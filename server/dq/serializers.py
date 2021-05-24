from rest_framework import serializers
from .models import Queue, DownloadJob


class QueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Queue
        fields = ("id", "name", "paused")


class DownloadJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = DownloadJob
        fields = (
            "id",
            "target_directory",
            "target_file",
            "url",
            "queue",
            "completed",
            "priority",
            "progress",
        )
