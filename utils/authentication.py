# !/usr/bin/env python
# -*- coding:utf-8 -*-
# project name: FastApiTest
# author: "Lei Yong" 
# creation time: 2020/6/30 17:58
# Email: leiyong711@163.com

import os
import json
import jinja2
from fastapi import Header
from utils.log import logger
from utils.Email import send_email
from config.base_config import WS_POLL_GROUP
from mydbs.redis_connect import get_redis_data
from utils.common_utils import verify_auth_token
from utils.exception_handling import UnicornException


global pid
pid = os.getpid()


async def token_is_true(token: str = Header(..., description="token验证")):
    """签名验证，全局使用"""
    Authorization = token
    if not Authorization:
        raise UnicornException(msg_code=401, error="非法操作！")
    sign = await verify_auth_token(Authorization)
    if not sign:
        raise UnicornException(msg_code=401, error="登录失效")
    token = get_redis_data(f"user:token:{sign['id']}")
    if token != Authorization:
        raise UnicornException(msg_code=401, error="非法操作！")
    return sign


async def send_sms_oneself(phone, code, sms_type):
    """
    利用自己手机发送短信验证码
    :param phone: 待发送手机号
    :param code: 验证码
    :param sms_type: 验证码类型
    :return:
    """
    smsType = ['', '[注册]', '[登录]', '[修改信息]', '[重置密钥]', '[重置密码]']
    sms = f'【XXX】尊敬的用户，您的{smsType[sms_type]}验证码为{code}，请于3分钟内正确输入，如非本人操作，请忽略此短信。'
    content = {"messageType": "SMS", "message": {"phone": phone, "sms": sms}}
    for wbs in WS_POLL_GROUP["SMS"]:
        await WS_POLL_GROUP["SMS"][wbs].send_text(json.dumps(content))
    logger.info(f"{pid} 进程  WebSocket 发短信推送完成")


async def send_email_oneself(email, code, email_type):
    """
    发送邮件键验证码
    :param email: 待发送邮箱
    :param code: 验证码
    :param email_type: 验证码类型
    :return:
    """
    logger.debug(os.getcwd())
    TemplateLoader = jinja2.FileSystemLoader(searchpath=os.getcwd())
    # 2.创建环境变量
    TemplateEnv = jinja2.Environment(loader=TemplateLoader)
    # 3.加载模板，渲染数据
    template = TemplateEnv.get_template('templates/Email.html')
    emailType = ['', '【注册验证码】', '【登录验证码】', '【修改信息验证码】', '【重置密钥验证码】', '【重置密码验证码】']
    text = template.render(companyName="测试", type=emailType[email_type], code=code)
    send_email(email, template=text)
    logger.info(f"{pid} 进程 发邮件完成")


async def sms_code_verify(phone, code):
    """
    验证短信验证码
    :param phone: 手机号
    :param code: 短信验证码
    :return:
    """
    redis_code = get_redis_data(f"sms:{phone}:code")
    if code == redis_code:
        return True
    return False
