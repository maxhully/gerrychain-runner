import collections
import os

from functools import partial

from .queue import Queue
from .chain import run_chain

DEFAULT_CONFIG = {"host": "localhost"}


def wait_for_tasks(queue):
    while True:
        get_task_and_run(queue)


def get_task_and_run(queue):
    task = queue.get_next_task()

    task_key = task.id
    update_status_callback = partial(queue.update_status, task_key)

    try:
        run_chain(task, update_status_callback)
    except Exception as err:
        queue.return_failed_task(task, err)


def main():
    queue_config = collections.ChainMap(os.environ, DEFAULT_CONFIG)
    queue = Queue(queue_config)

    wait_for_tasks(queue)


if __name__ == "__main__":
    main()
