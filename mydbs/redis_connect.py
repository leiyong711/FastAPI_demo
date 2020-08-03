# !/usr/bin/env python
# -*- coding:utf-8 -*-
# project name: FastApiTest
# author: "Lei Yong" 
# creation time: 2020/7/8 16:18
# Email: leiyong711@163.com

import redis
from config.base_config import REDIS_CONNECT

redistogo_url = REDIS_CONNECT

if not redistogo_url:
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    REDIS_PWD = '123456'
    REDIS_USER = None
else:
    redis_url = redistogo_url
    redis_url = redis_url.split('redis://')[1]
    redis_url = redis_url.split('/')[0]
    REDIS_USER, redis_url = redis_url.split(':', 1)
    REDIS_PWD, redis_url = redis_url.split('@', 1)
    REDIS_HOST, REDIS_PORT = redis_url.split(':', 1)


def redis_connect(db=3):
    """
    Established an resid connection.
    """
    pool = redis.ConnectionPool(host=REDIS_HOST, port=int(
        REDIS_PORT), password=REDIS_PWD, db=db, retry_on_timeout=True, decode_responses=True)
    redis_client = redis.Redis(connection_pool=pool, decode_responses=True)
    return redis_client


def get_redis_data(keys):
    """
    获取数据
    :param keys:
    :return:
    """
    db_redis = redis_connect(db=1)
    data = db_redis.get(keys)
    db_redis.close()
    return data


def set_redis_data(keys, value, expire=False, expire_time=-1):
    """
    设置数据
    :param keys:
    :return:
    """
    db_redis = redis_connect(db=1)
    db_redis.set(keys,value)
    if expire:
        db_redis.expire(keys, expire_time)
    db_redis.close()


def del_redis_data(keys):
    """
    删除键
    :param keys:
    :return:
    """
    db_redis = redis_connect(db=1)
    db_redis.delete(keys)
    db_redis.close()