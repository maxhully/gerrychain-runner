def get_redis_config():
    DEFAULT_CONFIG = {
        "REDIS_SERVICE_HOST": "redis",
        "REDIS_SERVICE_PORT": 6379,
        "REDIS_DB": 0,
        "REDIS_PASSWORD": None,
        "REDIS_SSL": False,
    }
    config = DEFAULT_CONFIG
    return {
        "host": config["REDIS_SERVICE_HOST"],
        "port": int(config["REDIS_SERVICE_PORT"]),
        "db": int(config["REDIS_DB"]),
        "password": config["REDIS_PASSWORD"],
        "ssl": bool(config["REDIS_SSL"]),
    }
