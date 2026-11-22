from app.core.exceptions import RegraNegocioError
from app.extensions import db
from app.models import AtendimentoAuditoria, Senha, StatusSenha
from app.services import relogio
from app.services.maquina_estados import transitar

S = StatusSenha


class AtendimentoService:
    def __init__(self, agora=None):
        self.agora = agora or relogio.agora

    def _carregar(self, senha_id: int):
        senha = db.session.get(Senha, senha_id)
        if senha is None:
            raise RegraNegocioError("Senha não encontrada.")
        aud = AtendimentoAuditoria.query.filter_by(senha_id=senha_id).first()
        if aud is None:
            raise RegraNegocioError("Senha ainda não foi chamada.")
        return senha, aud

    def chamar_novamente(self, senha_id: int, usuario_id=None) -> Senha:
        senha, aud = self._carregar(senha_id)
        try:
            transitar(senha, S.CHAMADA_NOVAMENTE, usuario_id)
            aud.horario_segunda_chamada = self.agora()
            db.session.commit()
            return senha
        except Exception:
            db.session.rollback()
            raise

    def iniciar(self, senha_id: int, usuario_id=None) -> Senha:
        senha, aud = self._carregar(senha_id)
        try:
            transitar(senha, S.EM_ATENDIMENTO, usuario_id)
            aud.horario_inicio_atendimento = self.agora()
            db.session.commit()
            return senha
        except Exception:
            db.session.rollback()
            raise

    def encerrar(self, senha_id: int, usuario_id=None) -> Senha:
        senha, aud = self._carregar(senha_id)
        try:
            transitar(senha, S.ATENDIDA, usuario_id)
            aud.horario_finalizacao_atendimento = self.agora()
            db.session.commit()
            return senha
        except Exception:
            db.session.rollback()
            raise

    def nao_compareceu(self, senha_id: int, usuario_id=None) -> Senha:
        senha, _ = self._carregar(senha_id)
        try:
            transitar(senha, S.NAO_COMPARECEU, usuario_id)
            db.session.commit()
            return senha
        except Exception:
            db.session.rollback()
            raise
        