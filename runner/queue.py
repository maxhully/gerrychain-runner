import json

from redis import StrictRedis
from .models import Run


class Queue:
    def __init__(self, redis_config, key="queue", Cache=StrictRedis):
        self.redis = Cache(**redis_config)
        self.key = key

    def ping(self):
        return self.redis.ping()

    def get_next_task(self):
        response = None
        while response is None:
            response = self.redis.brpop(self.key, timeout=1)
        key, task_json = response
        run_spec = json.loads(task_json)
        return Run(run_spec)

    def update_status(self, task_key, message):
        self.redis.set(task_key, json.dumps({"id": task_key, "status": message}))

    def return_failed_task(self, task, err=None):
        if "attempts" not in task:
            task["attempts"] = 0
        task["attempts"] += 1
        self.update_status(task["id"], "Failed. Retrying...")
        self.redis.rpush(json.dumps(task))
