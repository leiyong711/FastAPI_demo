# !/usr/bin/env python
# -*- coding:utf-8 -*-
# project name: FastApiTest
# author: "Lei Yong" 
# creation time: 2020/6/22 13:39
# Email: leiyong711@163.com
# from gevent import monkey; monkey.patch_all()
import os
import logging
import uvicorn
from api.v1 import create_app
from utils.log import logger
# from utils.utils import ws_push
from fastapi.responses import ORJSONResponse
from mydbs.redis_connect import redis_connect
from starlette.templating import Jinja2Templates
from config.base_config import WS_HEARTBEAT_TIMEOUT
from fastapi.exceptions import RequestValidationError
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from starlette.exceptions import HTTPException as StarletteHTTPException
from utils.exception_handling import UnicornException
app = create_app()


# 屏蔽定时任务INFO级日志
logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.ERROR)
logging.getLevelName(os.environ.get("LOG_LEVEL", "DEBUG"))

# 创建一个templates（模板）对象，以后可以重用。
templates = Jinja2Templates(directory="templates")


def redis_initialize():
    """
    redis数据库初始化
    :return:
    """
    db_redis = redis_connect(db=3)
    db_redis.delete('ws_connect_number')
    db_redis.delete('ws_sms_subscription_number')
    db_redis.close()
    logger.info("redis初始化完成")


@app.on_event('startup')
async def init_scheduler():
    """初始化"""
    redis_initialize()
    scheduler = AsyncIOScheduler()
    scheduler.add_job(func="api.v1.websocket.webSocket:heartbeatDetection", id="WebSocket服务心跳检测", args=(WS_HEARTBEAT_TIMEOUT,), trigger="interval", seconds=5)
    # scheduler.add_job(func="utils.utils:binding_fun", id="WebSocket消息推送触发", args=(ws_push,), trigger="interval", seconds=1)
    scheduler.add_job(func="utils.ws_utils:subscribe", id="redis订阅消息")
    scheduler.start()
    logger.info("启动调度器...")


@app.on_event("shutdown")
async def shutdown():
    logger.info("结束")


@app.exception_handler(UnicornException)
@app.exception_handler(StarletteHTTPException)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print(request.headers)
    if isinstance(exc, UnicornException):
        return ORJSONResponse({"code": exc.code, "message": exc.msg, "data": exc.error})
    if isinstance(exc, StarletteHTTPException):
        """
        HTTP错误
        """
        headers = request.headers["User-Agent"]
        data = exc.detail
        for i in ["Mozilla", "Chrome", "Safari"]:
            if i in headers:
                return templates.TemplateResponse("404.html", {"request": request, "id": id})
        return ORJSONResponse({"code": 500, "message": "失败", "data": str(data)})
    elif isinstance(exc, RequestValidationError):
        """
        参数验证错误
        """
        data = exc.errors()[0]["msg"]
        logger.error(f"{str(request.url).replace(str(request.base_url),'/')}  {str(exc.errors()[0]['loc'])} {str(data)} param=>{str(exc.body)}")
        return ORJSONResponse({"code": 500, "message": "失败", "data": f"{str(exc.errors()[0]['loc'])} {str(data)}"})
    else:
        """
        未知错误
        """
        data = "内部异常"
        logger.error(f"{str(request.url).replace(str(request.base_url), '/')}  {data}")
        return ORJSONResponse({"code": 500, "message": "失败", "data": data})


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8888,
        # reload=True,
    )
