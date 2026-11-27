import random

from app.extensions import db
from app.models import Senha, StatusSenha
from app.services import relogio

TAXA_NAO_ATENDIDAS = 0.05


class DescarteService:
    def __init__(self, agora=None):
        self.agora = agora or relogio.agora

    def descartar_sobras(self) -> int:
        """Fim do expediente: descarta senhas que sobraram aguardando."""
        sobras = Senha.query.filter(
            Senha.status_atual == StatusSenha.AGUARDANDO,
            Senha.descartada_em.is_(None),
        ).all()
        for s in sobras:
            s.descartada_em = self.agora()
            s.motivo_descarte = "FIM_EXPEDIENTE"
        db.session.commit()
        return len(sobras)

    def descartar_por_desistencia(self, rng=random.random) -> int:
        """Simula os ~5% de senhas que o cliente nunca usa (desistência)."""
        candidatas = Senha.query.filter(
            Senha.status_atual == StatusSenha.AGUARDANDO,
            Senha.descartada_em.is_(None),
        ).all()
        total = 0
        for s in candidatas:
            if rng() < TAXA_NAO_ATENDIDAS:
                s.descartada_em = self.agora()
                s.motivo_descarte = "DESISTENCIA"
                total += 1
        db.session.commit()
        return total