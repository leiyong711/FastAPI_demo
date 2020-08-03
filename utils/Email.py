# !/usr/bin/env python
# -*- coding:utf-8 -*-
# project name: FastAPI_demo
# author: "Lei Yong" 
# creation time: 2020/7/29 17:05
# Email: leiyong711@163.com

import os
import datetime
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr
from email.utils import formataddr
import smtplib
import traceback
from utils.log import logger


def retry_send(retry_num=3):
    def decorator(func):
        def wrapper(*args, **kw):
            att = 0
            while att < retry_num:
                try:
                    return func(*args, **kw)
                except Exception as e:
                    print(f'{e}, 重试]')
                    att += 1
            logger.error("经过多次尝试，邮件无法发送，停止发送")
        return wrapper
    return decorator


@retry_send()
def send_email(to_addr, template=None):
    """
    :param to_addr: 发件人，多个发件人用“,”分割，如：a@163.com,b@163.com,c@163.com
    :param template: 消息模板
    :return:
    """
    # sender = 'redmine@ipfz.com'  # 发件人
    # my_pass = 'Bituan@2019Red'  # 授权码
    # SMTP_SERVER = 'smtp.exmail.qq.com'  # 发件人邮箱中的'SMTP'服务器
    # PORT = 465  # ，端口是25端口是25

    sender = 'leiyonghn@163.com'
    # my_pass = 'QRVBKDUELCSHRIMR'
    my_pass = 'PTNPWLSZTUBNGFDB'
    SMTP_SERVER = 'smtp.163.com'
    PORT = 465

    def _format_addr(s):
        name, addr = parseaddr(s)
        # return formataddr((Header(name, 'utf-8').encode(), addr.encode('utf-8') if isinstance(addr, unicode) else addr))
        b = formataddr(
            (Header(name, 'utf-8').encode(),
             addr))
        return b

    # 创建一个带附件的实例
    message = MIMEMultipart()
    message['From'] = _format_addr(u'XX项目 <{}>'.format(sender))  # 发件人名字Last indulge
    message['To'] = to_addr  # 收件人名字
    message['Subject'] = Header(f'【XX项目】', 'utf-8').encode()  # 邮件主题

    # message.attach(MIMEText(nei, 'plain', 'utf-8'))
    message.attach(MIMEText(template, _subtype='html', _charset='utf-8'))

    try:
        server = smtplib.SMTP_SSL(SMTP_SERVER, PORT)  # 发件人邮箱中的'SMTP'服务器，端口是25
        server.set_debuglevel(0)

        server.login(sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.sendmail(sender, to_addr.split(','), message.as_string())
        # 关闭连接
        server.quit()
        logger.debug('邮件发送成功')

    except smtplib.SMTPException as e:
        logger.warning('发送邮件异常\n' + traceback.format_exc())
        raise Exception("邮件无法发送")
