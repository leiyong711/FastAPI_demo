# !/usr/bin/env python
# -*- coding:utf-8 -*-
# project name: FastApiTest
# author: "Lei Yong" 
# creation time: 2020/6/30 16:07
# Email: leiyong711@163.com

from typing import Dict, Any

import orjson
from pydantic import BaseModel, typing


# 正常的响应模板
from starlette.background import BackgroundTask
from starlette.responses import JSONResponse


class CORJSONResponse(JSONResponse):
    msg = "OK"
    msg_code = 0

    def __init__(
            self,
            content: typing.Any = None,
            status_code: int = 200,
            headers: dict = None,
            media_type: str = None,
            background: BackgroundTask = None,
            msg: str = None,
            msg_code: int = 200
    ) -> None:
        self.msg = msg if msg else self.msg
        self.msg_code = msg_code if msg_code else self.msg_code
        super().__init__(content, status_code, headers, media_type, background)

    def render(self, content: Any) -> bytes:
        reps_data = {
            "msg_code": self.msg_code,
            "msg": self.msg,
            "data": content
        }
        assert orjson is not None, "orjson must be installed to use ORJSONResponse"
        return orjson.dumps(reps_data)


# 成功的响应模板
class SucceedOut(CORJSONResponse):
    msg_code: int = 200
    msg: str = "成功"
    content: Any = None


# 错误的响应模板
class ErrorOUt(BaseModel):
    message: str = "失败"
    code: int = 500
    data: Any = None

