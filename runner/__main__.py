from .queue import Queue
from .config import get_redis_config
from .chain import run


def wait_for_tasks(queue):
    while True:
        print("Waiting for runs...")
        get_task_and_run(queue)


def send_message_and_log(queue, task_key):
    def callback(message):
        print(task_key + " | " + message)
        queue.send_message(task_key, message)

    return callback


def get_task_and_run(queue):
    task = queue.get_next_task()

    task_key = task.id
    callback = send_message_and_log(queue, task_key)

    try:
        result = run(task, callback)
        queue.complete_task(task_key, result)
    except Exception as err:
        queue.return_failed_task(task, err)


def main():
    print("Starting runner...")
    queue = Queue(get_redis_config())

    wait_for_tasks(queue)


if __name__ == "__main__":
    main()
