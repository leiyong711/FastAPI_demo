# !/usr/bin/env python
# -*- coding:utf-8 -*-
# project name: FastAPI_demo
# author: "Lei Yong" 
# creation time: 2020/8/3 10:42
# Email: leiyong711@163.com

import time
import traceback
from utils.exception_handling import ParameterError
from utils.log import logger
from model.db_models import *
from fastapi import APIRouter
from utils.common_utils import params_dispose, random_password
from mydbs.redis_connect import get_redis_data, set_redis_data
from model.api_model.user_params_model import *
from model.api_model import SucceedOut, ErrorOUt
from utils.authentication import send_sms_oneself, send_email_oneself

verify_api = APIRouter()


@verify_api.post("/getSMSCode", summary="获取短信验证码", tags=["验证相关"], responses={422: {'model': ErrorOUt}})
async def userLogin(*, smsCode: SMSCode):
    try:
        params = await params_dispose(smsCode.dict())
        if params["type"] < 1 or params["type"] > 5:
            return SucceedOut(msg_code=500, msg="失败", content="验证码类型错误")
        sms_type = params.pop("type")
        if sms_type != 1:
            db_mysql = SessionLocal()
            user = db_mysql.query(Member).filter_by(**params).first()
            if not user:
                return SucceedOut(msg_code=201, msg="失败",content="账户不存在")
        timer = int(time.time())
        last_time_send_time = get_redis_data(f"sms:{params['phone']}:sendTime")
        sms_send_frequency = get_redis_data(f"sms:{params['phone']}:frequency")
        last_time_send_time = int(last_time_send_time) if last_time_send_time else 0
        sms_send_frequency = int(sms_send_frequency) if sms_send_frequency else 0

        if sms_send_frequency >= 7:
            return SucceedOut(msg_code=201, msg="失败", content="当日获取验证码已超限")

        if (timer - last_time_send_time) < 180 and last_time_send_time != 0:
            # await send_sms_oneself(phone=user.phone, type=sms_type, code=sms_code)
            return SucceedOut(msg_code=201, msg="失败", content="验证码三分钟内有效，请勿重复获取")

        sms_code = await random_password(6)
        await send_sms_oneself(phone=params['phone'], sms_type=sms_type, code=sms_code)
        # 向redis插入手机验证码
        set_redis_data(f"sms:{params['phone']}:code", sms_code, True, 180)
        # 向redis插入发送验证码时间
        set_redis_data(f"sms:{params['phone']}:sendTime", timer, True, 86400)
        # 向redis修改当日发送次数
        set_redis_data(f"sms:{params['phone']}:frequency", sms_send_frequency + 1, True, 86400)
        return SucceedOut(msg_code=200, msg="成功", content={})
    except Exception:
        logger.error('获取短信验证码异常\n' + traceback.format_exc())
        return ParameterError(content="运行时异常")


@verify_api.post("/getEmailCode", summary="获取邮箱验证码", tags=["验证相关"], responses={422: {'model': ErrorOUt}})
async def userLogin(*, emailCode: EmailCode):
    try:
        params = await params_dispose(emailCode.dict())
        if params["type"] < 1 or params["type"] > 5:
            return SucceedOut(msg_code=500, msg="失败", content="验证码类型错误")
        email_type = params.pop("type")
        if email_type != 1:
            db_mysql = SessionLocal()
            user = db_mysql.query(Member).filter_by(**params).first()
            if not user:
                return SucceedOut(msg_code=201, msg="失败",content="账户不存在")
        timer = int(time.time())
        last_time_send_time = get_redis_data(f"email:{params['email']}:sendTime")
        email_send_frequency = get_redis_data(f"email:{params['email']}:frequency")
        last_time_send_time = int(last_time_send_time) if last_time_send_time else 0
        email_send_frequency = int(email_send_frequency) if email_send_frequency else 0

        if email_send_frequency >= 7:
            return SucceedOut(msg_code=201, msg="失败", content="当日获取验证码已超限")

        if (timer - last_time_send_time) < 180 and last_time_send_time != 0:
            # await send_sms_oneself(phone=user.phone, type=sms_type, code=sms_code)
            return SucceedOut(msg_code=201, msg="失败", content="验证码三分钟内有效，请勿重复获取")

        email_code = await random_password(6)
        await send_email_oneself(email=params['email'], code=email_code, email_type=email_type)
        # 向redis插入手机验证码
        set_redis_data(f"email:{params['email']}:code", email_code, True, 180)
        # 向redis插入发送验证码时间
        set_redis_data(f"email:{params['email']}:sendTime", timer, True, 86400)
        # 向redis修改当日发送次数
        set_redis_data(f"email:{params['email']}:frequency", email_send_frequency + 1, True, 86400)
        return SucceedOut(msg_code=200, msg="成功", content={})
    except Exception:
        logger.error('获取邮箱验证码异常\n' + traceback.format_exc())
        return ParameterError(content="运行时异常")
