# !/usr/bin/env python
# -*- coding:utf-8 -*-
# project name: FastAPI_demo
# author: "Lei Yong" 
# creation time: 2020/7/23 16:39
# Email: leiyong711@163.com

from model.api_model import CORJSONResponse


class ParameterError(CORJSONResponse):
    msg_code = 500
    msg = "失败"


class UnicornException(Exception):
    def __init__(self, error: str, msg_code: int = 500, msg: str = "失败"):
        self.code = msg_code
        self.msg = msg
        self.error = error
