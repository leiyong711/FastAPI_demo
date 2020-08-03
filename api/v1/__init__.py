# !/usr/bin/env python
# -*- coding:utf-8 -*-
# project name: FastAPI_demo
# author: "Lei Yong" 
# creation time: 2020/7/29 16:08
# Email: leiyong711@163.com

from fastapi import FastAPI
from model.db_models import Base, engine
from api.v1.websocket.webSocket import routes
from model.api_model import CORJSONResponse
from api.v1.test_app.test_user import user_test_api
from api.v1.test_app.verification_system import verify_api
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
                  redoc_url=redoc_url,
                  default_response_class=CORJSONResponse
                  )
    # 路由注册
    # api.include_router(user_api, prefix="/api")
    app.include_router(user_test_api, prefix="/api")
    app.include_router(verify_api, prefix="/api")
    Base.metadata.create_all(bind=engine)
    return app
