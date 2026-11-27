from argon2 import PasswordHasher

from app.core.exceptions import RegraNegocioError
from app.extensions import db
from app.models import Perfil, Usuario
from app.services.descarte_service import DescarteService

ph = PasswordHasher()


class AdminService:
    def descartar_sobras(self) -> int:
        return DescarteService().descartar_sobras()

    def criar_usuario(self, nome, matricula, login, senha, perfil) -> Usuario:
        if Usuario.query.filter(
            (Usuario.login == login) | (Usuario.matricula == matricula)
        ).first():
            raise RegraNegocioError("Login ou matrícula já cadastrados.")
        usuario = Usuario(
            nome=nome, matricula=matricula, login=login,
            senha_hash=ph.hash(senha), perfil=Perfil(perfil),
        )
        db.session.add(usuario)
        db.session.commit()
        return usuario