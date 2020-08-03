# !/usr/bin/env python
# -*- coding:utf-8 -*-
# project name: FastAPI_demo
# author: "Lei Yong" 
# creation time: 2020/7/24 11:01
# Email: leiyong711@163.com

import os
import json
import jinja2
import asyncio
import traceback
from utils.log import logger
from config.base_config import WS_POOL, WS_POLL_GROUP
from mydbs.redis_connect import redis_connect


async def redis_push(content):
    """
    向 redis 推送订阅消息
    :param content:
    :return:
    """
    try:
        db_redis = redis_connect(db=2)
        ps = db_redis.publish()
        ps.publish('websocket', content)
    except Exception:
        logger.info("redis消息推送异常\n" + traceback.format_exc())


class RedisPull:

    async def redisPull(self):
        """
        redis 订阅消息
        :return:
        """
        try:
            # 获取当前进程ID
            global pid
            pid = os.getpid()

            db_redis = redis_connect(db=2)
            ps = db_redis.pubsub()
            ps.subscribe("websocket")

            for item in ps.listen():
                if item["type"] == 'message':
                    content = item['data']
                    # 开始推送
                    for wbs in WS_POOL:
                        await WS_POOL[wbs][1].send_text(content)
                    logger.info(f"{pid} 进程  WebSocket 推送完成")
        except Exception:
            logger.info("redis消息订阅异常\n" + traceback.format_exc())


def subscribe():
    new_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(new_loop)
    loop = asyncio.get_event_loop()
    RP = RedisPull()
    loop.run_until_complete(RP.redisPull())


