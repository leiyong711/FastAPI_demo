# !/usr/bin/env python
# -*- coding:utf-8 -*-
# project name: FastAPI_demo
# author: "Lei Yong" 
# creation time: 2020/7/23 15:33
# Email: leiyong711@163.com

import traceback
from typing import List
from utils.log import logger
from model.db_models import *
from utils.ws_utils import redis_push
from fastapi import APIRouter, Depends
from model.api_model.params_model import *
from utils.common_utils import params_dispose
from model.api_model.user_params_model import *
from model.api_model import SucceedOut, ErrorOUt
from utils.exception_handling import ParameterError
from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from mydbs.redis_connect import set_redis_data, del_redis_data
from utils.authentication import token_is_true, sms_code_verify
from utils.common_utils import generate_auth_token, get_psswd_sign, verify_user_sign


user_test_api = APIRouter()


@user_test_api.post("/register", summary="注册", tags=["用户相关"], include_in_schema=True, responses={422: {'model': ErrorOUt}})
async def register(*, registerdb: UserRegisterIn):
    try:
        params = await params_dispose(registerdb.dict())
        password = params.pop("password")
        db_mysql = SessionLocal()
        user = db_mysql.query(Member).filter_by(**params).first()
        if not user:
            # params["passwd"] = sign_md5(password)
            if 'phone' in params.keys():
                if sms_code_verify(params["phone"], params["code"]) in False:
                    return SucceedOut(msg_code=201, msg="失败", content="验证码错误")
            elif 'email' in params.keys():
                pass
            elif 'name' in params.keys():
                pass
            else:
                return SucceedOut(msg_code=500, msg="失败", content="参数不完整")
            params["passwd"] = await get_psswd_sign(password)
            result = Member(**params)
            db_mysql.add(result)
            db_mysql.commit()
            db_mysql.refresh(result)
            return SucceedOut(content="成功")
        else:
            return SucceedOut(content="数据已存在")
    except Exception:
        logger.error('用户注册异常\n' + traceback.format_exc())
        return ParameterError(content="运行时异常")


@user_test_api.post("/login", summary="登录", tags=["用户相关"], responses={422: {'model': ErrorOUt}})
async def userLogin(*, user_login: UserLoginIn):
    try:
        params = await params_dispose(user_login.dict())
        params_copy = params.copy()
        password = params.pop("password")
        unit_type = params.pop("type")
        if 'phone' in params.keys():
            if sms_code_verify(params["phone"], params["code"]) in False:
                return SucceedOut(msg_code=201, msg="失败", content="验证码错误")
        elif 'email' in params.keys():
            pass
        elif 'name' in params.keys():
            pass
        else:
            return SucceedOut(msg_code=500, msg="失败", content="参数不完整")
        db_mysql = SessionLocal()
        user = db_mysql.query(Member).filter_by(**params).first()
        if not user:
            return SucceedOut(msg_code=201, msg="失败",content="账户不存在")

        if await verify_user_sign(password, user.passwd) is False:
            return SucceedOut(msg_code=200, msg="失败", content="账户与密码不匹配")

        sign = await generate_auth_token(**params_copy)
        set_redis_data(f"user:token:{user.id}", sign)
        data = {"id": user.id, "token": sign}
        return SucceedOut(msg_code=200, msg="成功", content=data)
    except Exception:
        logger.error('用户登录异常\n' + traceback.format_exc())
        return ParameterError(content="运行时异常")


@user_test_api.get("/logout", summary="退出登录", tags=["用户相关"], responses={422: {'model': ErrorOUt}})
async def logout(*, token: str = Depends(token_is_true)):
    try:
        del_redis_data(f"user:token:{token['id']}")
        return SucceedOut(msg_code=200, msg="成功", content=None)
    except Exception:
        logger.error('用户退出登录异常\n' + traceback.format_exc())
        return ParameterError(content="运行时异常")


PydanticUser = sqlalchemy_to_pydantic(Solarenergyinput)  # ,exclude=["id"])
@user_test_api.post("/selectDB", summary="数据库查询", tags=["数据库操作测试"], response_model=List[PydanticUser],  responses={422: {'model': ErrorOUt}})
async def selectDB(*, selectdb: SelectDBIn, token: str = Depends(token_is_true)):
    try:
        logger.error(f"token ==> {token}")
        params = await params_dispose(selectdb.dict())
        if len(params) == 2:
            # 分页查询
            db_mysql = SessionLocal()
            user = db_mysql.query(Solarenergyinput).limit(params["page"]).offset(params["page"] * (params["size"] -1)).all()
        else:
            query_params = params.copy()
            del query_params["page"]
            del query_params["size"]
            db_mysql = SessionLocal()
            user = db_mysql.query(Solarenergyinput).filter_by(**query_params).limit(params["page"]).offset(params["page"] * (params["size"] -1)).all()
            await redis_push(str(user))
        return user
    except Exception:
        logger.error('查询数据异常\n' + traceback.format_exc())
        return ParameterError(content="运行时异常")
