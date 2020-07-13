# !/usr/bin/env python
# -*- coding:utf-8 -*-
# project name: FastApiTest
# author: "Lei Yong" 
# creation time: 2020/6/30 16:14
# Email: leiyong711@163.com

# 项目名称
TITLE = "XXX 项目"

# 项目版本
VERSION = "1.0.0"

# 接口交互文档
API_DOCS = True

# 数据库连接配置
DB_CONNECT = "mysql://test:123456@127.0.0.1:3306/fastapiTest?charset=utf8"

# redis数据库配置
REDIS_CONNECT = "redis://test:123456@127.0.0.1:6379"

# WebSocket对象连接池
WS_POOL = {}

# WebSocket心跳超时时间（单位s）
WS_HEARTBEAT_TIMEOUT = 10

# TOKEN 加盐
SALT = 'TEST'

# TOKEN 超时时间
TOKEN_TIMEOUT = 3000
