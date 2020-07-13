# !/usr/bin/env python
# -*- coding:utf-8 -*-
# project name: FastApiTest
# author: "Lei Yong" 
# creation time: 2020/6/29 15:37
# Email: leiyong711@163.com

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.base_config import DB_CONNECT

SQLALCHEMY_DATABASE_URL = DB_CONNECT

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_recycle=7200,  # 默认为 -1, 推荐设置为 7200, 即如果 connection 空闲了 7200 秒，自动重新获取，以防止 connection 被 db server 关闭。
    pool_size=1,  # 连接数大小，默认为 5，正式环境该数值太小，需根据实际情况调大
    max_overflow=1,  # 超出 pool_size 后可允许的最大连接数，默认为 10, 这 10 个连接在使用过后，不放在 pool 中，而是被真正关闭的。
    pool_timeout=30,  # 获取连接的超时阈值，默认为 30 秒
    isolation_level="READ UNCOMMITTED"  # 取消缓存机制
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
