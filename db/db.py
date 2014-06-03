# -*- coding: utf-8 -*-

import redis
import Conf

# 连接redis
def connectRedis():
    redisConfig = Conf.redis
    redis_conn = redis.Redis(
            host = redisConfig["host"],
            port = redisConfig["port"],
            charset = 'utf-8')
    try:
        redis_conn.ping()
    except redis.exceptions.ConnectionError, e:
        logger.error("Connect to Redis failed: {0}".format(e))
        raise
    else:
        return redis_conn


if __name__ == '__main__':
    redis_conn = connectRedis()
