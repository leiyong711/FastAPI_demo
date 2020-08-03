# !/usr/bin/env python
# -*- coding:utf-8 -*-
# project name: FastApiTest
# author: "Lei Yong" 
# creation time: 2020/7/1 10:55
# Email: leiyong711@163.com

import random
import hashlib
from threading import Thread
from utils.log import logger
from passlib.context import CryptContext
from config.base_config import SALT, TOKEN_TIMEOUT
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def random_password(number):
    """
    生成随机数字验证码
    :return:
    """
    code_list = random.sample(range(0, 9), number)
    code = ''.join([str(x) for x in code_list])
    return code


async def params_dispose(params):
    """入参模板处理 去除为 None 字段"""
    logger.info("入参 ==> " + str(params))
    for key in list(params.keys()):
        if not params.get(key) and params[key] != 0.0:
            del params[key]
    logger.info("参数处理后 ==> " + str(params))
    return params


async def convert(data):
    """
    将字典的键&值从byte类型转换为str类型
    :param data:
    :return:
    """
    if isinstance(data, bytes):return data.decode('utf-8')
    if isinstance(data, dict):return dict(map(convert, data.items()))
    if isinstance(data, tuple):return map(convert, data)
    return data


async def asyncFun(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper


# 生成Token
async def generate_auth_token(expiration=TOKEN_TIMEOUT, **data):
    s = Serializer(SALT, expires_in=expiration)
    return s.dumps(data).decode()


# 解密Token
async def verify_auth_token(token,expiration=TOKEN_TIMEOUT):
    s = Serializer(SALT, expires_in=expiration)
    try:
        data = s.loads(token)
    except Exception:
        data = None
    return data


async def sign_md5(data):
    """
    MD5加密
    :param data:
    :return:
    """
    md = hashlib.md5()
    md.update(data.encode(encoding='utf-8'))
    sign = md.hexdigest()
    logger.debug('MD5加密前：' + data)
    logger.debug('MD5加密后：' + sign)
    return sign


async def get_psswd_sign(passwd):
    """
    加密
    :param passwd:
    :return:
    """
    sign = pwd_context.hash(passwd)
    logger.warning(sign)
    return sign


async def verify_user_sign(passwd, sign):
    """
    解密
    :param passwd: 密码
    :param sign: 加密后密码
    :return:
    """
    logger.warning(pwd_context.verify(passwd, sign))
    return pwd_context.verify(passwd, sign)
