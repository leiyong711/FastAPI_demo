# !/usr/bin/env python
# -*- coding:utf-8 -*-
# project name: FastApiTest
# author: "Lei Yong" 
# creation time: 2020/7/1 10:55
# Email: leiyong711@163.com

import os
import time
import json
import asyncio
import traceback
from threading import Thread
from utils.log import logger
from config.base_config import WS_POOL
from config.redis_connect import redis_connect


def params_dispose(params):
    """入参模板处理 去除为 None 字段"""
    logger.info("入参 ==> " + str(params))
    for key in list(params.keys()):
        if not params.get(key) and params[key] != 0.0:
            del params[key]
    logger.info("参数处理后 ==> " + str(params))
    return params


def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


def callback_fun(func):
    """
    创建异步任务
    :param func:
    :return:
    """
    def wrapper(*args, **kwargs):
        new_loop = asyncio.new_event_loop()
        t = Thread(target=start_loop, args=(new_loop,))
        t.start()
        asyncio.run_coroutine_threadsafe(func(*args, **kwargs), new_loop)
    return wrapper


async def binding_fun(func, *args, **kwargs):
    """
    定时执行取对应进程 redis 缓存推送任务
    :param func:
    :param args:
    :param kwargs:
    :return:
    """
    # 查询当前进程是否还未推送
    db_redis = redis_connect(db=3)
    send_pid = db_redis.hkeys('ws_send_pid')
    db_redis.close()

    # 获取当前进程ID
    global pid
    pid = os.getpid()

    for key in send_pid:
        if int(key) == pid:
            func(*args, **kwargs)
            logger.info(f"{pid} 进程  回调函数创建成功")

            # 推送完成 删除该进程任务缓存
            db_redis = redis_connect(db=3)
            db_redis.hdel('ws_send_pid', key)
            db_redis.close()


@callback_fun
async def ws_push():
    """
    给socket用户推送消息
    :return:
    """
    try:
        # 取 redis 取推送内容
        db_redis = redis_connect(db=3)
        data = db_redis.get("ws_push_msg")
        db_redis.close()

        # 插装自定义参数
        data = json.loads(data)
        data["time"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

        # 开始推送
        for wbs in WS_POOL:
            await WS_POOL[wbs][1].send_text(json.dumps(data))
        logger.info(f"{pid} 进程  WebSocket 推送完成")
    except Exception:
        logger.info("推送WebSocket消息失败 ==> " + traceback.format_exc())







