# FastAPI_demo
基础框架
```
目录结构说明

├─ app
│	└─ v1  版本
│	 	├─ __init__.py  视图注册
│	    ├─ test_app  基本逻辑
│	    │	├─ __init__.py
│	    │	├─ test_api.py  测试程序
│	    │	└─ verification_system.py  验证码相关
│	    └─ websocket
│	    	├─ __init__.py
│	    	└─ webSocket.py   推送消息
├─ config   配置文件
│	├─ __init__.py
│	└─ base_config.py  基础配置
├─ logs  日志存储目录
├─ model  模板
│	├─ __init__.py
│	├─ db_models.py  MySQL数据库表模型
│	└─ api_model  请求类模板
│	 	├─ __init__.py  接口响应模板
│	 	└─ params_model.py  接口入参模型
├─ mydbs   数据库
│	├─ mysql_connect.py  mysql数据库
│	└─ redis_connect.py  redis数据库
├─ templates   静态文件
│	├─ 404.html
│	├─ Email.html  验证码邮件模板
│	└─ test.html
├─ utils 工具文件
│ 	├─ authentication.py  验证鉴权
│ 	├─ common_utils.py  公用工具
│ 	├─ Email.py  邮件
│ 	├─ exception_handling.py  自定义异常
│ 	├─ log.py  日志文件
│ 	└─ ws_utils.py  redis订阅相关
├─ main.py  入口文件
├─ requirements.txt  用到的第三方库
└─ README.md
```

启动方式
>开发环境部署,直接运行python3 main.py文件

>生产环境部署
>gunicorn  main:app -w 20 --threads=10 -k  uvicorn.workers.UvicornWorker -b 0.0.0.0:80
