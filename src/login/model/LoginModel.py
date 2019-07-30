
import os
import hashlib
import json
import datetime

from .entities.Login import UsuarioClave, LoginLog, Device

class LoginModel:

    def login(self, session, user: str, password: str, device_id: str, challenge:str):
        usr = session.query(UsuarioClave).filter(UsuarioClave.usuario == user, UsuarioClave.clave == password, UsuarioClave.eliminada == None).one_or_none()
        l = LoginLog()
        l.created = datetime.datetime.utcnow()
        l.challenge = challenge
        l.device_id = device_id
        l.usuario = user
        l.clave = '' if usr else password
        l.status = usr is not None
        session.add(l)
        return usr

    def _generate_hash(self, seed:str):
        salt = os.urandom(5)
        data = f'{salt}{seed}'.encode('utf8')
        return hashlib.sha256(data).hexdigest()

    def generate_device(self, session, description:str, device_data:dict):
        d = Device()
        d.created = datetime.datetime.utcnow()
        d.description = description
        d.data = json.dumps(device_data)
        d.hash_ = self._generate_hash(d.data)
        session.add(d)
        return d.hash_