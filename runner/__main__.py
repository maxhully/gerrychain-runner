import logging

from .queue import Queue
from .config import get_redis_config
from .chain import run_chain

log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)


def wait_for_tasks(queue):
    while True:
        log.info("Waiting for runs...")
        get_task_and_run(queue)


def send_message_and_log(queue, task_key):
    def callback(message):
        log.info(task_key + " | " + message)
        queue.send_message(task_key, message)

    return callback


def get_task_and_run(queue):
    task = queue.get_next_task()

    task_key = task.id
    callback = send_message_and_log(queue, task_key)

    try:
        run_chain(task, callback)
    except Exception as err:
        queue.return_failed_task(task, err)

    queue.complete_task(task_key)


def main():
    log.info("Starting runner...")
    queue = Queue(get_redis_config())

    wait_for_tasks(queue)


if __name__ == "__main__":
    main()
