import logging

from .queue import Queue
from .chain import run_chain

DEFAULT_CONFIG = {"host": "localhost"}

log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)


def wait_for_tasks(queue):
    while True:
        log.info("Waiting for runs...")
        get_task_and_run(queue)


def update_status_and_log(queue, task_key):
    def callback(message):
        log.info(task_key + " | " + message)
        queue.update_status(task_key, message)

    return callback


def get_task_and_run(queue):
    task = queue.get_next_task()

    task_key = task.id
    callback = update_status_and_log(queue, task_key)

    try:
        run_chain(task, callback)
    except Exception as err:
        queue.return_failed_task(task, err)


def main():
    log.info("Starting runner...")
    queue_config = DEFAULT_CONFIG
    queue = Queue(queue_config)

    wait_for_tasks(queue)


if __name__ == "__main__":
    main()
