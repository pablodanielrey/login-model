
from .entities.Login import UsuarioClave

class LoginModel:

    def login(self, session, user: str, password: str, device_id: str) {
        usr = session.query(UsuarioClave).filter(UsuarioClave.usuario == user, UsuarioClave.clave == password).one_or_none()
        if not usr:
            
    }