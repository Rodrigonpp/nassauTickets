from sqlalchemy import select

from app.extensions import db
from app.models import EstadoFila, Senha, StatusSenha, TipoSenha


class FilaRepository:
    def travar_estado_fila(self) -> EstadoFila:
        """Bloqueia a linha única de controle até o fim da transação."""
        estado = db.session.execute(
            select(EstadoFila).where(EstadoFila.id == 1).with_for_update()
        ).scalar_one_or_none()
        if estado is None:
            estado = EstadoFila(id=1)
            db.session.add(estado)
            db.session.flush()
        return estado

    def proxima_aguardando(self, tipo: TipoSenha) -> Senha | None:
        return db.session.execute(
            select(Senha)
            .where(
                Senha.tipo_senha == tipo,
                Senha.status_atual == StatusSenha.AGUARDANDO,
                Senha.descartada_em.is_(None),
            )
            .order_by(Senha.data_hora_emissao, Senha.id)
            .limit(1)
            .with_for_update(skip_locked=True)
        ).scalar_one_or_none()