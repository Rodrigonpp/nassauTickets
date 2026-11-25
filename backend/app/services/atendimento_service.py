from datetime import timedelta

from flask import current_app
from sqlalchemy import select

from app.core.exceptions import RegraNegocioError
from app.extensions import db
from app.models import AtendimentoAuditoria, Senha, StatusSenha
from app.services import relogio
from app.services.maquina_estados import transitar
from app.services.tm import duracao_simulada_min

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
            inicio = aud.horario_inicio_atendimento or self.agora()
            aud.horario_finalizacao_atendimento = inicio + timedelta(
                minutes=duracao_simulada_min(senha.tipo_senha)
            )
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


    def processar_prazos(self) -> int:
        """Aplica o prazo de comparecimento a cada chamada.

        CHAMADA há mais de PRAZO_CHAMADA_SEGUNDOS  -> CHAMADA_NOVAMENTE
        CHAMADA_NOVAMENTE há mais de PRAZO         -> NAO_COMPARECEU (expirada)

        A hora gravada da 2ª chamada é a do vencimento do prazo (e não a hora em
        que esta rotina rodou), então o histórico fica correto mesmo que ninguém
        tenha consultado a API na hora exata. Retorna quantas transições fez.
        """
        prazo = timedelta(seconds=current_app.config["PRAZO_CHAMADA_SEGUNDOS"])
        agora = self.agora()
        try:
            linhas = db.session.execute(
                select(Senha, AtendimentoAuditoria)
                .join(AtendimentoAuditoria, AtendimentoAuditoria.senha_id == Senha.id)
                .where(Senha.status_atual.in_([S.CHAMADA, S.CHAMADA_NOVAMENTE]))
                .with_for_update()
            ).all()

            transicoes = 0
            for senha, aud in linhas:
                if senha.status_atual == S.CHAMADA:
                    if aud.horario_primeira_chamada is None:
                        continue
                    vencimento = aud.horario_primeira_chamada + prazo
                    if vencimento > agora:
                        continue
                    transitar(senha, S.CHAMADA_NOVAMENTE)
                    aud.horario_segunda_chamada = vencimento
                    transicoes += 1

                if senha.status_atual == S.CHAMADA_NOVAMENTE:
                    base = aud.horario_segunda_chamada or aud.horario_primeira_chamada
                    if base is not None and base + prazo <= agora:
                        transitar(senha, S.NAO_COMPARECEU)
                        transicoes += 1

            if transicoes:
                db.session.commit()
            else:
                db.session.rollback()  # só para liberar os locks
            return transicoes
        except Exception:
            db.session.rollback()
            raise