# !/usr/bin/env python
# -*- coding:utf-8 -*-
# project name: FastAPI_demo
# author: "Lei Yong" 
# creation time: 2020/7/28 13:48
# Email: leiyong711@163.com

from pydantic import BaseModel, Field


class UserLoginIn(BaseModel):
    """
    用户登录接口入参模板
    """
    name: str = Field(None, title="用户名", min_length=4, max_length=10, regex="^[A-Za-z0-9]+$")
    phone: str = Field(None, title="手机号", regex="^(13[0-9]|14[5|7]|15[0|1|2|3|5|6|7|8|9]|18[0|1|2|3|5|6|7|8|9])\d{8}$")
    email: str = Field(None, title="邮箱", regex="^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$")
    password: str = Field(..., title="密码", regex="^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,10}$")
    type: str = Field(None, title="登录类型", example="WEB")
    code: str = Field(..., title="验证码", min_length=6, max_length=6, regex="^[0-9]+$")


class UserRegisterIn(BaseModel):
    """
    用户注册接口入参模板
    """
    name: str = Field(None, title="用户名", min_length=4, max_length=10, regex="^[A-Za-z0-9]+$")
    phone: str = Field(None, title="手机号", regex="^(13[0-9]|14[5|7]|15[0|1|2|3|5|6|7|8|9]|18[0|1|2|3|5|6|7|8|9])\d{8}$")
    email: str = Field(None, title="邮箱", regex="^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$")
    password: str = Field(..., title="密码", regex="^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,10}$")
    code: str = Field(..., title="验证码", min_length=6, max_length=6, regex="^[0-9]+$")


class SMSCode(BaseModel):
    """
    获取短信验证码
    """
    # phone: str = Field(..., title="手机号", regex="^(13[0-9]|14[5|7]|15[0|1|2|3|5|6|7|8|9]|18[0|1|2|3|5|6|7|8|9])\d{8}$")
    phone: str = Field(..., title="手机号", regex="^1(?:70\d|(?:9[89]|8[0-24-9]|7[135-8]|66|5[0-35-9])\d|3(?:4[0-8]|[0-35-9]\d))\d{7}$")
    # smsType: int = Field(..., title="验证码类型", regex="^[0-9]+$")
    type: int = Field(..., title="验证码类型")


class EmailCode(BaseModel):
    """
    获取邮箱验证码
    """
    email: str = Field(..., title="邮箱", regex="^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$")
    type: int = Field(..., title="验证码类型")

