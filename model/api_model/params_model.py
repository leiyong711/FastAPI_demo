# !/usr/bin/env python
# -*- coding:utf-8 -*-
# project name: FastApiTest
# author: "Lei Yong" 
# creation time: 2020/6/22 16:44
# Email: leiyong711@163.com

from pydantic import BaseModel, Field


class UserRegisterIn(BaseModel):
    """
    用户接口入参模板
    """
    name: str = Field(..., title="用户名")
    password: str = Field(..., title="密码", regex="^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,10}$")


class UserIn(BaseModel):
    """
    用户接口入参模板
    """
    username: str = Field(..., title="用户名")
    password: str = Field(..., title="密码")
    email: str = Field(None, title="邮箱", min_length=10)
    full_name: str = None


class InsetDBIn(BaseModel):
    """
    数据库新增数据接口入参模板
    """
    voltage: float = Field(..., title="电压")
    electricity: float = Field(..., title="电流")


class UpdateDBIn(BaseModel):
    """
    数据库修改接口入参模板
    """
    id: int = Field(..., title="数据ID")
    voltage: float = Field(..., title="电压")
    electricity: float = Field(None, title="电流")
    created_at: str = Field(None, title="创建时间")


class SelectDBIn(BaseModel):
    """
    数据库查询接口入参模板
    """
    id: int = Field(None, title="数据ID")
    voltage: float = Field(None, title="电压")
    electricity: float = Field(None, title="电流")
    page: int = Field(None, title="当前页码", gt=0, lt=21)
    size: int = Field(None, title="每页数量", gt=0)
    created_at: str = Field(None, title="创建时间")


class DelectDBIn(BaseModel):
    """
    数据库删除接口入参模板
    """
    id: int = Field(..., title="数据ID")
