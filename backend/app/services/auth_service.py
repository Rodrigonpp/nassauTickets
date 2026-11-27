from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from flask_jwt_extended import create_access_token

from app.core.exceptions import NaoAutenticadoError
from app.extensions import db
from app.models import LogAcesso, Usuario

ph = PasswordHasher()


class AuthService:
    def login(self, login: str, senha: str, ip: str | None = None) -> dict:
        usuario = Usuario.query.filter_by(login=login).first()
        ok = False
        if usuario and usuario.ativo:
            try:
                ok = ph.verify(usuario.senha_hash, senha)
            except VerifyMismatchError:
                ok = False

        # LGPD: registra toda tentativa (sem gravar a senha)
        db.session.add(
            LogAcesso(
                usuario_id=usuario.id if usuario else None,
                acao="LOGIN_OK" if ok else "LOGIN_FALHA",
                ip=ip,
            )
        )
        db.session.commit()

        if not ok:
            # mensagem genérica: não revela se o login existe
            raise NaoAutenticadoError("Login ou senha inválidos.")

        token = create_access_token(
            identity=str(usuario.id),
            additional_claims={"perfil": usuario.perfil.value, "nome": usuario.nome},
        )
        return {
            "access_token": token,
            "perfil": usuario.perfil.value,
            "nome": usuario.nome,
            "usuario_id": usuario.id,
        }