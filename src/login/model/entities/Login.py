import uuid

from pulsar.schema import JsonSchema, Record, String
from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, Float, func, or_
from login.model.entities import Base

from enum import Enum

class LoginEventTypes(Enum):
    CHANGE_CREDENTIALS = 'CHANGE_CREDENTIALS'
    LOGIN = 'LOGIN'
    LOGOUT = 'LOGOUT'

class LoginEvent(Record):
    """ Evento para pulsar """
    type_ = String()
    username = String()
    credentials = String()


def generateId():
    return str(uuid.uuid4())

class UserCredentials(Base):

    __tablename__ = 'user_credentials'

    id = Column(String, primary_key=True, default=generateId)
    created = Column(DateTime())
    updated = Column(DateTime())

    user_id = Column(String, nullable=False)
    username = Column(String)
    credentials = Column(String)
    expiration = Column(DateTime)
    deleted = Column(DateTime)
    temporal = Column(Boolean, default=False)


class UserHash(Base):

    __tablename__ = 'user_hash'

    id = Column(String, primary_key=True, default=generateId)
    created = Column(DateTime())

    user_id = Column(String())
    hash_ = Column(String())


class LoginLog(Base):
    __tablename__ = 'login_log'

    id = Column(String(), primary_key=True, default=generateId)
    created = Column(DateTime())

    username = Column(String())
    credentials = Column(String())

    hash_ = Column(String())

    challenge = Column(String())
    device_id = Column(String())

    status = Column(Boolean())


class UserPositionLog(Base):
    __tablename__ = 'user_position_log'

    id = Column(String(), primary_key=True, default=generateId)
    created = Column(DateTime())

    user_id = Column(String())
    longitude = Column(Float())
    latitude = Column(Float())
    timestamp = Column(Integer())


class Device(Base):
    __tablename__ = 'devices'

    id = Column(String(), primary_key=True, default=generateId)
    created = Column(DateTime())

    description = Column(String())
    data = Column(String())

    hash_ = Column(String())

