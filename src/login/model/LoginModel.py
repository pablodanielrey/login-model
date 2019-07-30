
import datetime

from .entities.Login import UsuarioClave, LoginLog

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