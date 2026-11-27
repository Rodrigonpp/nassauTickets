from sqlalchemy import select

from app.extensions import db
from app.models import AtendimentoAuditoria, Guiche, Senha


class PainelService:
    def ultimas_chamadas(self, limite: int = 5):
        momento = db.func.coalesce(
            AtendimentoAuditoria.horario_segunda_chamada,
            AtendimentoAuditoria.horario_primeira_chamada,
        )
        linhas = db.session.execute(
            select(Senha, AtendimentoAuditoria, Guiche)
            .join(AtendimentoAuditoria, AtendimentoAuditoria.senha_id == Senha.id)
            .outerjoin(Guiche, Guiche.id == AtendimentoAuditoria.guiche_id)
            .where(AtendimentoAuditoria.horario_primeira_chamada.is_not(None))
            .order_by(momento.desc(), AtendimentoAuditoria.id.desc())
            .limit(limite)
        ).all()

        return [
            {
                "numero_senha": senha.numero_senha,
                "tipo_senha": senha.tipo_senha.value,
                "sequencial": senha.sequencial_diario,
                "guiche": guiche.numero_guiche if guiche else None,
                "ultima_chamada": aud.horario_segunda_chamada is not None,
                "status_atual": senha.status_atual.value,
                "chamada_em": (aud.horario_segunda_chamada or aud.horario_primeira_chamada),
            }
            for senha, aud, guiche in linhas
        ]