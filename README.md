
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=tomaso_download-queue&metric=alert_status)](https://sonarcloud.io/dashboard?id=tomaso_download-queue)

# download-queue
Simple downloader with web frontend

## What it is

This app manages multiple queues of files that are downloaded to a certain
folder on the server.

## What it is not

There are no fancy features like multi-source download, multi-protocol etc.

## Deployment

TBD.


## Development

Python and Django paths are always a bit tricky so to play with job processor 
I recommend to install python libraries first with pipenv and then setup paths
like this:

```
$ cd job_processor
$ pipenv install
$ pipenv shell
$ export PYTHONPATH=$PWD/../server
$ export DJANGO_SETTINGS_MODULE=server.settings
$ ipython3 
In [1]: import django
In [2]: django.setup()
In [3]: from dq import models
In [4]: models.Queue.objects.all()
```


