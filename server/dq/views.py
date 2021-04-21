from django.shortcuts import render
from rest_framework import viewsets
from .serializers import QueueSerializer, DownloadJobSerializer
from .models import Queue, DownloadJob

# Create your views here.

class QueueView(viewsets.ModelViewSet):
    serializer_class = QueueSerializer
    queryset = Queue.objects.all()

class DownloadJobView(viewsets.ModelViewSet):
    serializer_class = DownloadJobSerializer
    queryset = DownloadJob.objects.all()
