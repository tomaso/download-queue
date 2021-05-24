#!/usr/bin/python3
import django
import logging
import os.path
import requests
import time

django.setup()

from dq import models


def setup_logging() -> None:
    logging.basicConfig(
        format="%(asctime)s %(levelname)s %(message)s", level=logging.DEBUG
    )


def setup() -> None:
    """
    Initial setup of the daemon
    """
    setup_logging()


def loop() -> None:
    """
    TODO: use async methods here and go parallel
    """
    logging.debug("Getting all incomplete jobs")
    all_jobs = models.DownloadJob.objects.filter(completed__exact=False)
    logging.debug(f"There are {len(all_jobs)} incomplete jobs")
    if not all_jobs:
        logging.debug("There is no incomplete job - sleeping for 5s")
        time.sleep(5)
    for q in models.Queue.objects.all():
        candidate_jobs = q.downloadjob_set.filter(completed__exact=False)
        logging.debug(
            f"Queue: {q.name}: Number of incomplete jobs: {len(candidate_jobs)}"
        )
        for dj in candidate_jobs:
            logging.debug(
                f"Queue: {q.name}: Going to download {dj.target_file} from {dj.url} to {dj.target_directory}"
            )
            url = dj.url
            file_name = os.path.join(dj.target_directory, dj.target_file)
            with open(file_name, "wb") as f:
                logging.debug(f"{file_name} opened for writing")
                response = requests.get(url, stream=True)
                total_length = response.headers.get("content-length")
                if total_length is None:
                    f.write(response.content)
                else:
                    dl = 0
                    total_length = int(total_length)
                    for data in response.iter_content(chunk_size=1024 * 1024):
                        dl += len(data)
                        f.write(data)
                        progress = int(100 * dl / total_length)
                        dj.progress = progress
                        dj.save()
                        logging.debug(f"{dj.target_file}: progress: {dj.progress}%")
                    dj.completed = True
                    dj.save()


def main() -> None:
    """
    TODO: parse arguments
    """
    try:
        setup()
    except Exception as exc:
        print(f"Setup of the daemon failed: {exc}")
    termination_requested = False
    while not termination_requested:
        try:
            loop()
        except KeyboardInterrupt:
            logging.debug("Termination requested with Ctrl-c")
            termination_requested = True


if __name__ == "__main__":
    main()
