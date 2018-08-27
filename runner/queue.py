import json

from redis import Redis


class Queue:
    def __init__(self, redis_uri, key="queue"):
        self.redis = Redis(redis_uri)
        self.key = key

    def get_next_task(self):
        return self.redis.brpop(self.key)

    def update_status(self, task_key, message):
        self.redis.set(task_key, message)

    def return_failed_task(self, task):
        task["attempts"] += 1
        self.redis.rpush(json.dumps(task))
