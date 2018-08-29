import os
import collections


def get_redis_config():
    DEFAULT_CONFIG = {
        "REDIS_HOST": "localhost",
        "REDIS_PORT": 6379,
        "REDIS_DB": 0,
        "REDIS_PASSWORD": None,
        "REDIS_SSL": False,
    }
    config = collections.ChainMap(os.environ, DEFAULT_CONFIG)
    return {
        "host": config["REDIS_HOST"],
        "port": int(config["REDIS_PORT"]),
        "db": int(config["REDIS_DB"]),
        "password": config["REDIS_PASSWORD"],
        "ssl": bool(config["REDIS_SSL"]),
    }
