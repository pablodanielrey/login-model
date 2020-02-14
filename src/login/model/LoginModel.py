
import os
import hashlib
import json
import datetime
import uuid

from .entities.Login import UserCredentials, LoginLog, Device, UserHash, UserPositionLog

class LoginModel:

    def login_hash(self, session, hash_:str, device_id:str, challenge:str, position:None) -> UserHash:
        h = session.query(UserHash).filter(UserHash.hash_ == hash_).one_or_none()
        if h:
            uid = h.user_id
            uc = session.query(UserCredentials).filter(UserCredentials.user_id == uid, UserCredentials.deleted == None).one()

            lid = str(uuid.uuid4())
            lcreated = datetime.datetime.utcnow()

            l = LoginLog()
            l.id = lid
            l.created = lcreated
            l.challenge = challenge
            l.device_id = device_id
            l.hash_ = hash_
            l.usuario = uc.usuario
            l.status = True
            session.add(l)

            if position:
                p = UserPositionLog()
                p.id = lid
                p.created = lcreated
                p.user_id = uid
                p.longitude = position['longitude'] if 'longitude' in position else 0.0
                p.latitude = position['latitude'] if 'latitude' in position else 0.0
                p.timestamp = position['timestamp'] if 'timestamp' in position else 0
                session.add(p)

        else:
            l = LoginLog()
            l.created = datetime.datetime.utcnow()
            l.challenge = challenge
            l.device_id = device_id
            l.hash_ = hash_
            l.status = False
            session.add(l)

        return h

    def login(self, session, user: str, password: str, device_id: str, challenge:str, position=None):

        usr = session.query(UserCredentials).filter(UserCredentials.username == user, UserCredentials.credentials == password, UserCredentials.deleted == None).one_or_none()
        hash_ = None

        lid = str(uuid.uuid4())
        lcreated = datetime.datetime.utcnow()

        if usr and usr.user_id:
            ''' si no tiene hash le genero uno '''
            uid = usr.user_id
            h = session.query(UserHash).filter(UserHash.user_id == uid).one_or_none()
            if not h:
                hash_ = self._generate_hash(uid)
                h = UserHash()
                h.created = datetime.datetime.utcnow()
                h.user_id = usr.user_id
                h.hash_ = hash_
                session.add(h)
            else:
                hash_ = h.hash_

            if position:
                p = UserPositionLog()
                p.id = lid
                p.created = lcreated
                p.user_id = uid
                p.longitude = position['longitude'] if 'longitude' in position else 0.0
                p.latitude = position['latitude'] if 'latitude' in position else 0.0
                p.timestamp = position['timestamp'] if 'timestamp' in position else 0
                session.add(p)

        l = LoginLog()
        l.id = lid
        l.created = lcreated
        l.challenge = challenge
        l.device_id = device_id
        l.usuario = user
        l.clave = '' if usr else password
        l.status = usr is not None
        session.add(l)

        return usr, hash_

    def _generate_hash(self, seed:str):
        salt = os.urandom(5)
        data = f'{salt}{seed}'.encode('utf8')
        return hashlib.sha256(data).hexdigest()

    def generate_device(self, session, description:str, device_data:dict):
        d = Device()
        d.created = datetime.datetime.utcnow()
        d.description = description
        try:
            d.data = json.dumps(device_data)
        except Exception:
            d.data = ''
        d.hash_ = self._generate_hash(d.data)
        session.add(d)
        return d.hash_

    def get_device_by_hash(self, session, hash_:str):
        d = session.query(Device).filter(Device.hash_ == hash_).one()
        return d