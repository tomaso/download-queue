#!/usr/bin/python3
import asyncio

from asyncio.queues import Queue
from asyncio.tasks import Task
import aiofiles
import aiohttp
import django
import logging
import os.path
import requests
import time

django.setup()

from asgiref.sync import sync_to_async
from dq import models
from typing import Awaitable, List
import tempfile


def setup_logging() -> None:
    logging.basicConfig(
        format="%(asctime)s %(levelname)s %(message)s", level=logging.DEBUG
    )
    filename = tempfile.mktemp()  # Noncompliant
    tmp_file = open(filename, "w+")


def setup() -> None:
    """
    Initial setup of the daemon
    """
    setup_logging()


async def process_one_job(download_job: models.DownloadJob) -> None:
    url = download_job.url
    async with aiofiles.open(
        os.path.join(download_job.target_directory, download_job.target_file), mode="wb"
    ) as f:
        progress = 0
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                assert response.status == 200
                content_length = int(response.content_length)
                done_length = 0
                while True:
                    try:
                        chunk = await asyncio.shield(response.content.read(1024))
                    except asyncio.TimeoutError:
                        logging.error(
                            f"Timeout occurred when downloading {url} - retrying"
                        )
                        continue
                    if not chunk:
                        break
                    await f.write(chunk)
                    done_length += len(chunk)
                    last_progress = progress
                    progress = (100 * done_length) // content_length
                    download_job.progress = progress
                    await sync_to_async(download_job.save, thread_sensitive=True)()
                    logging.debug(
                        f"{download_job.target_file}: progress: {download_job.progress}%"
                    )
                    if progress - last_progress > 1:
                        logging.info(
                            f"{download_job.target_file}: progress: {download_job.progress}%"
                        )
                download_job.completed = True
                download_job.progress = 100
                await sync_to_async(download_job.save, thread_sensitive=True)()


def process_one_job_sync(download_job: models.DownloadJob) -> None:
    logging.info(
        f"Queue: {download_job.queue.name}: Going to download {download_job.target_file} from {download_job.url} to {download_job.target_directory}"
    )
    url = download_job.url
    file_name = os.path.join(download_job.target_directory, download_job.target_file)
    with open(file_name, "wb") as f:
        logging.info(f"{file_name} opened for writing")
        response = requests.get(url, stream=True)
        total_length = response.headers.get("content-length")
        if total_length is None:
            f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=1024):
                dl += len(data)
                f.write(data)
                progress = int(100 * dl / total_length)
                download_job.progress = progress
                download_job.save()
                logging.debug(
                    f"{download_job.target_file}: progress: {download_job.progress}%"
                )
            download_job.completed = True
            download_job.save()


async def process_candidate_jobs(candidate_jobs: List[models.DownloadJob]) -> None:
    await asyncio.gather(*[process_one_job(dj) for dj in candidate_jobs])


def loop() -> None:
    """ """
    logging.debug("Getting all incomplete jobs")
    all_jobs = models.DownloadJob.objects.filter(completed__exact=False)
    logging.debug(f"There are {len(all_jobs)} incomplete jobs")
    if not all_jobs:
        logging.debug("There is no incomplete job - sleeping for 5s")
        time.sleep(5)
    candidate_jobs = []
    # TODO: optimize the loop (normally thiswould be one SQL query)
    for q in models.Queue.objects.all():
        job = q.downloadjob_set.filter(completed__exact=False).first()
        logging.debug(f"Queue: {q.name}: Selected job: {job}")
        if job:
            candidate_jobs.append(job)
    asyncio.run(process_candidate_jobs(candidate_jobs))


async def download_task_from_queue(queue: models.Queue) -> Task:
    job = queue.downloadjob_set.filter(completed__exact=False).first()
    if job:
        t = process_one_job(job)
    else:
        logging.debug(f"Queue {queue} has no job to download -> going to sleep")
        t = asyncio.create_task(asyncio.sleep(5))
    await t
    return asyncio.create_task(download_task_from_queue(queue))


@sync_to_async
def get_queues():
    return list(models.Queue.objects.all())


async def queue_loop() -> None:
    """
    Create task for every queue
    """
    # TODO: optimize the loop (normally this would be one SQL query)
    tasks = []
    queues = await get_queues()
    logging.info(f"Queues: {queues}")
    for q in queues:
        tasks.append(asyncio.create_task(download_task_from_queue(q)))
    termination_requested = False
    while not termination_requested:
        try:
            t_new_tasks = []
            for t in tasks:
                t_new = await t
                t_new_tasks.append(t_new)
            tasks = t_new_tasks
        except KeyboardInterrupt:
            logging.info("Termination requested with Ctrl-c")
            termination_requested = True


def main() -> None:
    """ """
    try:
        setup()
    except Exception as exc:
        print(f"Setup of the daemon failed: {exc}")
    asyncio.run(queue_loop())


if __name__ == "__main__":
    main()
