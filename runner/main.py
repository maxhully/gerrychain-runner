import collections
import json
import os

from functools import partial

from .queue import Queue
from .chain import run_chain

DEFAULT_CONFIG = {"REDIS_KEY": "gerrychain-queue"}


def wait_for_tasks(queue):
    while True:
        task = json.loads(queue.get_next_task())

        task_key = task["id"]
        update_status_callback = partial(queue.update_status, task_key)

        try:
            run_chain(task, update_status_callback)
        except Exception:
            queue.return_failed_task(task)


def main():
    config = collections.ChainMap(os.environ, DEFAULT_CONFIG)
    queue = Queue(config["REDIS_URI"], config["REDIS_KEY"])

    wait_for_tasks(queue)


if __name__ == "__main__":
    main()
