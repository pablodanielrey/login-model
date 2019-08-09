import uuid
from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, Float, func, or_

from login.model.entities import Base

def generateId():
    return str(uuid.uuid4())

class UsuarioClave(Base):

    __tablename__ = 'usuario_clave'

    id = Column(String, primary_key=True, default=generateId)
    creado = Column(DateTime())
    actualizado = Column(DateTime())

    usuario_id = Column(String, nullable=False)
    usuario = Column(String)
    clave = Column(String)
    expiracion = Column(DateTime)
    eliminada = Column(DateTime)
    debe_cambiarla = Column(Boolean, default=False)
    dirty = Column(Boolean)
    google = Column(Boolean)


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

    usuario = Column(String())
    clave = Column(String())

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

