# !/usr/bin/env python
# -*- coding:utf-8 -*-
# project name: FastApiTest
# author: "Lei Yong" 
# creation time: 2020/6/22 16:35
# Email: leiyong711@163.com

from fastapi import FastAPI
from app.test_app.test_api import user_api
from app.websocket.webSocket import *
from model.db_models import Base, engine
from config.base_config import API_DOCS, TITLE, VERSION

# 是否开放API交互文档
if API_DOCS:
    docs_url = "/docs"
    redoc_url = "/redoc"
else:
    docs_url = None
    redoc_url = None


def create_app():
    app = FastAPI(routes=routes,
                  title=TITLE,
                  version=VERSION,
                  docs_url=docs_url,
                  redoc_url=redoc_url
                  )
    # 路由注册
    app.include_router(user_api, prefix="/api")
    Base.metadata.create_all(bind=engine)
    return app
