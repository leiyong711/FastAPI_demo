# FastAPI_demo
基础框架
```
目录结构说明

├─ app
│	├─ __init__.py  视图注册
│	├─ test_app
│	│	├─ __init__.py
│	│	└─ test_api.py  测试程序
│	└─ websocket
│	 	├─ __init__.py
│	 	└─ webSocket.py   推送消息
├─ config   配置文件
│	├─ __init__.py
│	├─ base_config.py  基础配置
│	├─ mysql_connect.py  MySQL连接
│	└─ redis_connect.py  redis连接
├─ logs  日志存储目录
├─ model  模板
│	├─ __init__.py
│	├─ db_models.py  MySQL数据库表模型
│	└─ response_model  请求类模板
│	 	├─ __init__.py  接口响应模板
│	 	└─ params_model.py  接口入参模型
├─ templates   静态文件
│	├─ 404.html
│	└─ test.html
├─ utils 工具文件
│ 	├─ authentication.py  token鉴权
│ 	├─ log.py  日志文件
│ 	└─ utils.py  公用方法
├─ main.py  入口文件
├─ requirements.txt  用到的第三方库
└─ README.md
```

启动方式
>开发环境部署,直接运行python3 main.py文件

>生产环境部署
>gunicorn  main:app -w 20 --threads=10 -k  uvicorn.workers.UvicornWorker -b 0.0.0.0:80
