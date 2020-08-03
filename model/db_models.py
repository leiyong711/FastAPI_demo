# coding: utf-8
# from sqlalchemy import Column, Float, String, TIMESTAMP, text
# from sqlalchemy.dialects.mysql import DATETIME, INTEGER
# from sqlalchemy.ext.declarative import declarative_base
#
# Base = declarative_base()
# metadata = Base.metadata
from mydbs.mysql_connect import Base, SessionLocal, engine
from sqlalchemy import Column, INTEGER, Float, TIMESTAMP, String, text


class Member(Base):
    __tablename__ = 'member'
    __table_args__ = {'comment': '用户'}

    id = Column(INTEGER, primary_key=True, comment='ID')
    phone = Column(String(20), nullable=True, unique=True, comment='手机号')
    email = Column(String(20), nullable=True, unique=True, comment='邮箱')
    name = Column(String(20), nullable=True, unique=True, comment='用户名')
    passwd = Column(String(128), nullable=False, comment='密码')
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='数据时间戳')


class Batteryout(Base):
    __tablename__ = 'batteryout'
    __table_args__ = {'comment': '电池输出'}

    id = Column(INTEGER, primary_key=True, comment='ID')
    voltage = Column(Float(asdecimal=True), comment='太阳能电压')
    electricity = Column(Float(asdecimal=True), comment='太阳能电流')
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='数据时间戳')


class Batteryvoltage(Base):
    __tablename__ = 'batteryvoltage'
    __table_args__ = {'comment': '电池信息'}

    id = Column(INTEGER, primary_key=True, comment='ID')
    voltage = Column(Float(asdecimal=True), comment='电池电压')
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='数据时间戳')


class Solarenergyinput(Base):
    __tablename__ = 'solarenergyinput'
    __table_args__ = {'comment': '输入'}

    id = Column(INTEGER, primary_key=True, comment='ID')
    voltage = Column(Float, nullable=False, comment='太阳能电压')
    electricity = Column(Float, nullable=False, comment='太阳能电流')
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='数据时间戳')


