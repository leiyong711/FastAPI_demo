# !/usr/bin/env python
# -*- coding:utf-8 -*-
# project name: FastApiTest
# author: "Lei Yong" 
# creation time: 2020/6/30 10:03
# Email: leiyong711@163.com

import os
import time
import json
from utils.log import logger
from config.base_config import WS_POOL, WS_POLL_GROUP
from starlette.responses import HTMLResponse
from mydbs.redis_connect import redis_connect
from starlette.routing import Route, WebSocketRoute
from starlette.endpoints import WebSocketEndpoint, HTTPEndpoint


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off" placeholder="" />
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            document.getElementById("messageText").placeholder="第一次输入内容为昵称";

            var ws = new WebSocket("ws://orangep.top:8088/ws/ws");

            // 接收
            ws.onmessage = function(event) {
                // 获取id为messages的ul标签内
                var messages = document.getElementById('messages')
                // 创建li标签
                var message = document.createElement('li')
                // 创建内容
                var content = document.createTextNode(event.data)
                // 内容添加到li标签内
                message.appendChild(content)
                // li标签添加到ul标签内
                messages.appendChild(message)
            };

            var name = 0;
            // 发送
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()

                if (name == 0){
                    document.getElementById("messageText").placeholder="";
                    name = 1;
                }
            }
        </script>
    </body>
</html>
"""


class Homepage(HTTPEndpoint):
    """
    测试模板
    """
    async def get(self, request):
        return HTMLResponse(html)


class Remov(HTTPEndpoint):
    async def get(self, request):
        key = request.query_params.get("id")
        return HTMLResponse("ok")


class Echo(WebSocketEndpoint):

    encoding = "text"

    async def alter_socket(self, websocket):
        """
        用内存地址生成连接用户名
        :param websocket:
        :return:
        """
        socket_str = str(websocket)[1:-1]
        socket_list = socket_str.split(' ')
        socket_only = socket_list[3]
        return socket_only

    async def on_connect(self, websocket):
        """
        连接成功
        :param websocket:
        :return:
        """
        await websocket.accept()
        # 用户输入名称
        # name = await websocket.receive_text()
        name = id(self)
        socket_only = await self.alter_socket(websocket)
        # 添加连接池 保存用户名
        WS_POOL[socket_only] = [f'{name}', websocket, int(time.time())]

    async def on_receive(self, websocket, data):
        """
        收发消息
        :param websocket:
        :param data:
        :return:
        """
        socket_only = await self.alter_socket(websocket)
        data = json.loads(data)
        if data["subType"] == "subscription":
            if data["messageType"] == "SMS":
                logger.info("订阅短信推送成功")
                WS_POLL_GROUP["SMS"][socket_only] = websocket

        elif data["subType"] == "heartbeat" and data["message"] == "ping":
            # logger.info(f"WebSocket收到 {socket_only} ID: {WS_POOL[socket_only][0]} 心跳 ==> {data}")
            # 更新心跳时间
            data = {"messageType": "heartbeat", "message": "pong"}
            WS_POOL[socket_only][2] = int(time.time())
            await WS_POOL[socket_only][1].send_text(json.dumps(data))
        else:
            logger.info(f"WebSocket收到 {WS_POOL[socket_only][0]} 消息 ==> {data}")

    async def on_disconnect(self, websocket, close_code):
        """
        关闭连接
        :param websocket:
        :param close_code: 错误码
        :return:
        """
        socket_only = await self.alter_socket(websocket)
        # 删除连接池
        WS_POOL.pop(socket_only)
        WS_POLL_GROUP["SMS"].pop(socket_only)


# 心跳检测
async def heartbeatDetection(heartbeat_time):
    """
    WebSocket心跳检测机制
    :param heartbeat_time: 心跳超时时间
    :return:
    """
    timer = int(time.time())

    # 存储心跳过期的连接
    temp = []

    # 检测心跳是否超时
    for key, value in WS_POOL.items():
        if timer - value[2] > heartbeat_time:
            temp.append(key)

    # 关闭心跳超时的连接
    for i in temp:
        try:
            logger.warning(f"{WS_POOL[i][0]} 心跳超时 {timer - WS_POOL[i][2]}")
            await WS_POOL[i][1].close(code=1002)
        except KeyError:
            pass

    # 获取当前进程ID
    pid = os.getpid()

    # 获取缓存中每个进程的连接数
    db_redis = redis_connect(db=3)
    db_redis.hset('ws_connect_number', pid, len(WS_POOL))
    db_redis.hset('ws_sms_subscription_number', pid, len(WS_POLL_GROUP["SMS"]))
    connect_number = db_redis.hgetall('ws_connect_number')
    sms_sub_number = db_redis.hgetall('ws_sms_subscription_number')
    db_redis.close()

    # 统计所有进程中的连接数
    connect_count = 0
    for key, value in connect_number.items():
        connect_count += int(value)

    sms_count = 0
    for key, value in sms_sub_number.items():
        sms_count += int(value)
    logger.debug(f"当前WebSocket 总连接数 {connect_count}, SMS订阅总数 {sms_count}")


routes = [
    Route("/ws", Homepage),
    Route("/remov", Remov),
    WebSocketRoute("/ws/ws", Echo),
]





