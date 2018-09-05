import json

from redis import StrictRedis
from .models import Run


class Queue:
    def __init__(self, redis_config, key="queue", Cache=StrictRedis, Task=Run):
        self.redis = Cache(**redis_config)
        self.Task = Task

        self.key = key
        self.statuses_key = key + "-statuses"

    def ping(self):
        return self.redis.ping()

    def get_next_task(self):
        response = None
        while response is None:
            response = self.redis.brpop(self.key, timeout=1)
        key, task_json = response
        task_spec = json.loads(task_json)
        self.update_status(task_spec["id"], "RUNNING")
        return self.Task(task_spec)

    def update_status(self, task_key, status):
        if status not in ("WAITING", "FAILED", "RUNNING", "COMPLETE"):
            raise ValueError(
                "Status is not one of 'WAITING', 'RUNNING', 'FAILED', or 'COMPLETE'"
            )
        self.redis.hset(self.statuses_key, task_key, status)
        self.send_message(task_key, "Status is set to {}".format(status))

    def send_message(self, task_key, message):
        self.redis.publish(channel=task_key, message=message)

    def return_failed_task(self, task):
        if "attempts" in task:
            task["failed_attempts"] += 1
        else:
            task["failed_attempts"] = 1
        self.redis.rpush(self.key, json.dumps(task))
        self.update_status(task["id"], "FAILED")

    def complete_task(self, task_key, return_value):
        self.update_status(task_key, "COMPLETE")
        self.redis.set(task_key + "-report", return_value)
