# !/usr/bin/env python
# -*- coding:utf-8 -*-
# project name: FastApiTest
# author: "Lei Yong" 
# creation time: 2020/6/30 16:07
# Email: leiyong711@163.com

from typing import Dict, Any
from pydantic import BaseModel


# 正常的响应模板
class SucceedOut(BaseModel):
    message: str = "成功"
    code: int = 0
    data: Any = None


# 错误的响应模板
class ErrorOUt(BaseModel):
    message: str = "失败"
    code: int = 500
    data: Any = None
