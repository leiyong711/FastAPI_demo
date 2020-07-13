# coding: utf-8
# from sqlalchemy import Column, Float, String, TIMESTAMP, text
# from sqlalchemy.dialects.mysql import DATETIME, INTEGER
# from sqlalchemy.ext.declarative import declarative_base
#
# Base = declarative_base()
# metadata = Base.metadata
from config.mysql_connect import Base, engine, SessionLocal
from sqlalchemy import Column, INTEGER, Float, TIMESTAMP, String, text


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


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'comment': 'The User model'}

    id = Column(INTEGER, primary_key=True, comment='ID')
    username = Column(String(20), nullable=False, unique=True, comment='???')
    name = Column(String(50), comment='??')
    family_name = Column(String(50))
    category = Column(String(30), nullable=False, server_default=text("'misc'"))
    password_hash = Column(String(128))
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))


