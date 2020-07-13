# !/usr/bin/env python
# -*- coding:utf-8 -*-
# project name: FastApiTest
# author: "Lei Yong" 
# creation time: 2020/6/22 16:36
# Email: leiyong711@163.com

import json
import time
import traceback
from utils.log import logger
from model.db_models import *
from fastapi import APIRouter
from utils.utils import params_dispose
from config.redis_connect import redis_connect
from model.response_model.params_model import *
from model.response_model import SucceedOut, ErrorOUt


db_mysql = SessionLocal()
user_api = APIRouter()


class AA(BaseModel):
    name: str=None
    password:str=None
    data = SucceedOut


@user_api.on_event("startup")
async def startup():
    """
    redis数据库初始化
    :return:
    """
    db_redis = redis_connect(db=3)
    db_redis.delete('ws_number_pid')
    db_redis.delete('ws_send_pid')
    db_redis.delete('ws_push_time')
    db_redis.delete('ws_push_msg')
    db_redis.close()
    logger.info("redis初始化完成")


@user_api.on_event("shutdown")
async def shutdown():
    logger.info("结束")


# @user_api.post("/user", response_model=Union[AA], summary="测试",)
@user_api.post("/user", response_model=AA, summary="测试", include_in_schema=True, responses={422: {'model': ErrorOUt}})
async def create_user(*, user: UserIn):
    logger.info("从网上")
    aa = AA(name='123', password='333')
    print(aa)
    # return user
    return SucceedOut(data=aa)
    # return JSONResponse(status_code=HTTP_201_CREATED, content=MyOut)



@user_api.post("/insetDB", summary="数据库新增测试", tags=["数据库操作测试"], include_in_schema=True, responses={422: {'model': ErrorOUt}})
async def insetDB(*, insetdb: InsetDBIn):
    try:
        params = params_dispose(insetdb.dict())
        result = Solarenergyinput(**params)
        db_mysql.add(result)
        db_mysql.commit()
        db_mysql.refresh(result)

        # db_redis = await get_class()
        db_redis = redis_connect(db=3)

        # await db_redis.set("ws_push_msg", json.dumps(params))
        db_redis.set("ws_push_msg", json.dumps(params))
        # await db_redis.set("ws_push_time", int(time.time()))
        push_time = int(time.time())
        db_redis.set("ws_push_time", push_time)
        t = db_redis.hgetall('ws_number_pid')
        db_redis.close()

        db_redis = redis_connect(db=3)
        for key, value in t.items():
            db_redis.hset('ws_send_pid', key, push_time)
        db_redis.close()


        return SucceedOut(data=True)
    except Exception:
        logger.error(traceback.format_exc())
        return SucceedOut(code=500, message="失败", data=False)


@user_api.post("/updateDB", summary="数据库修改", tags=["数据库操作测试"], include_in_schema=True, responses={422: {'model': ErrorOUt}})
async def updateDB(*, updatedb: UpdateDBIn):
    try:
        params = params_dispose(updatedb.dict())
        id = params.pop("id")
        result = db_mysql.query(Solarenergyinput).filter_by(id=id).first()
        for key in params:
            setattr(result, key, params.get(key))
        db_mysql.commit()
        return SucceedOut(data=True)
    except Exception:
        logger.error(traceback.format_exc())
        return SucceedOut(code=500, message="失败", data=False)


@user_api.post("/selectDB", summary="数据库查询", tags=["数据库操作测试"], include_in_schema=True, responses={422: {'model': ErrorOUt}})
async def selectDB(*, selectdb: SelectDBIn):
    try:
        params = params_dispose(selectdb.dict())
        if len(params) <= 2:
            # data = db.query(Solarenergyinput).all()
            # 分页查询
            data = db_mysql.query(Solarenergyinput).limit(params["page"]).offset(params["page"] * (params["size"] -1)).all()
        else:
            teams = db_mysql.query(Solarenergyinput).filter_by(**params).first()
            data = teams
        db_mysql.close()
        return SucceedOut(data=data)
    except Exception:
        logger.error(traceback.format_exc())
        return SucceedOut(code=500, message="失败", data=False)


@user_api.post("/deleteDB", summary="数据库删除", tags=["数据库操作测试"], include_in_schema=True, responses={422: {'model': ErrorOUt}})
async def deleteDB(*, delectdb: DelectDBIn):
    # db = SessionLocal()
    try:
        params = params_dispose(delectdb.dict())
        result = db_mysql.query(Solarenergyinput).filter_by(**params).first()
        if not result:
            return SucceedOut(code=500, message="失败", data="数据不存在")
        else:
            db_mysql.delete(result)
            db_mysql.commit()
            return SucceedOut(data=True)
    except Exception:
        logger.error(traceback.format_exc())
        return SucceedOut(code=500, message="失败", data=False)
