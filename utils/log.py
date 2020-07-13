# !/usr/bin/env python
# -*- coding:utf-8 -*-
# project name: FastApiTest
# author: "Lei Yong" 
# creation time: 2020/6/23 10:02
# Email: leiyong711@163.com

import os
import time
from loguru import logger


# INFO级日志模板初始化配置
logger.add(f"{os.path.join(os.getcwd(), 'logs')}/info_log_{time.strftime('%Y_%m_%d')}.log",
           level="INFO",
           format='{time:YYYY-MM-DD HH :mm:ss.SSS} - {level} - {file} - {function} - {line} - {message}',
           rotation="00:00",  # 文件过大就会重新生成一个新文件  "12:00"# 每天12点创建新文件
           encoding="utf-8",
           enqueue=True,  # 异步写入
           serialize=False,  # 序列化为json
           retention="10 days",  # 一段时间后会清空
           compression="zip"  # 保存为zip格式
           )

# ERROR级日志模板初始化配置
logger.add(f"{os.path.join(os.getcwd(), 'logs')}/error_log_{time.strftime('%Y_%m_%d')}.log",
           level="ERROR",
           format='{time:YYYY-MM-DD HH :mm:ss.SSS} - {level} - {file} - {message} - {function} - {line}',
           rotation="00:00",  # 文件过大就会重新生成一个新文件  "12:00"# 每天12点创建新文件
           encoding="utf-8",
           enqueue=True,  # 异步写入
           serialize=False,  # 序列化为json
           retention="10 days",  # 一段时间后会清空
           compression="zip"  # 保存为zip格式
           )
