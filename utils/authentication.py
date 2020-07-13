# !/usr/bin/env python
# -*- coding:utf-8 -*-
# project name: FastApiTest
# author: "Lei Yong" 
# creation time: 2020/6/30 17:58
# Email: leiyong711@163.com

from config.base_config import SALT, TOKEN_TIMEOUT
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


# 生成Token
def generate_auth_token(data, expiration=TOKEN_TIMEOUT):
    s = Serializer(SALT, expires_in=expiration)
    return s.dumps({"userName": data}).decode()


# 解密Token
def verify_auth_token(token,expiration=TOKEN_TIMEOUT):
    s = Serializer(SALT, expires_in=expiration)
    try:
        data = s.loads(token)["userName"]
    except Exception:
        data = None
    return data
