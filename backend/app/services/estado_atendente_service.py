from datetime import timedelta

from flask import current_app
from sqlalchemy import func, select

from app.extensions import db
from app.models import AtendimentoAuditoria, Senha, StatusSenha, TipoSenha
from app.services import relogio

# Mesmos status que impedem o atendente de chamar outra senha (ChamadaService)
EM_ANDAMENTO = [
    StatusSenha.CHAMADA,
    StatusSenha.CHAMADA_NOVAMENTE,
    StatusSenha.EM_ATENDIMENTO,
]


def _item(senha: Senha, aud: AtendimentoAuditoria) -> dict:
    return {
        "id": senha.id,
        "numero_senha": senha.numero_senha,
        "tipo_senha": senha.tipo_senha.value,
        "status_atual": senha.status_atual.value,
        "data_hora_emissao": senha.data_hora_emissao,
        "primeira_chamada_em": aud.horario_primeira_chamada,
        "ultima_chamada_em": (
            aud.horario_segunda_chamada or aud.horario_primeira_chamada
        ),
    }


class EstadoAtendenteService:
    def __init__(self, agora=None):
        self.agora = agora or relogio.agora

    def obter(self, usuario_id: int, limite: int = 5) -> dict:
        return {
            "fila": self._fila(),
            "atual": self._atual(usuario_id),
            "ultimas": self._ultimas(limite),
        }

    def _fila(self) -> dict:
        """Senhas aguardando por tipo (mesmo critério de proxima_aguardando)."""
        linhas = db.session.execute(
            select(Senha.tipo_senha, func.count(Senha.id))
            .where(
                Senha.status_atual == StatusSenha.AGUARDANDO,
                Senha.descartada_em.is_(None),
            )
            .group_by(Senha.tipo_senha)
        ).all()
        fila = {tipo.value: 0 for tipo in TipoSenha}
        for tipo, total in linhas:
            fila[tipo.value] = total
        return fila

    def _atual(self, usuario_id: int) -> dict | None:
        """Senha que este atendente chamou e ainda não finalizou."""
        linha = db.session.execute(
            select(Senha, AtendimentoAuditoria)
            .join(AtendimentoAuditoria, AtendimentoAuditoria.senha_id == Senha.id)
            .where(
                AtendimentoAuditoria.usuario_id == usuario_id,
                Senha.status_atual.in_(EM_ANDAMENTO),
            )
            .order_by(AtendimentoAuditoria.id.desc())
            .limit(1)
        ).first()
        if not linha:
            return None

        senha, aud = linha
        item = _item(senha, aud)
        item["prazo_segundos"] = current_app.config["PRAZO_CHAMADA_SEGUNDOS"]
        item["segundos_restantes"] = self._segundos_restantes(senha, aud)
        return item

    def _segundos_restantes(self, senha: Senha, aud: AtendimentoAuditoria):
        """Segundos até o próximo prazo (rechamada ou expiração).

        None quando a senha não tem prazo (já em atendimento).
        """
        if senha.status_atual == StatusSenha.CHAMADA:
            base = aud.horario_primeira_chamada
        elif senha.status_atual == StatusSenha.CHAMADA_NOVAMENTE:
            base = aud.horario_segunda_chamada or aud.horario_primeira_chamada
        else:
            return None
        if base is None:
            return None

        prazo = timedelta(seconds=current_app.config["PRAZO_CHAMADA_SEGUNDOS"])
        restante = (base + prazo - self.agora()).total_seconds()
        return max(0, int(restante))

    def _ultimas(self, limite: int) -> list[dict]:
        """Últimas senhas chamadas por qualquer atendente (mais recente primeiro)."""
        momento = func.coalesce(
            AtendimentoAuditoria.horario_segunda_chamada,
            AtendimentoAuditoria.horario_primeira_chamada,
        )
        linhas = db.session.execute(
            select(Senha, AtendimentoAuditoria)
            .join(AtendimentoAuditoria, AtendimentoAuditoria.senha_id == Senha.id)
            .where(AtendimentoAuditoria.horario_primeira_chamada.is_not(None))
            .order_by(momento.desc(), AtendimentoAuditoria.id.desc())
            .limit(limite)
        ).all()
        return [_item(senha, aud) for senha, aud in linhas]