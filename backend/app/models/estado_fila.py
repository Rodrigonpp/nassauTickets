from typing import Optional

from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column

from app.extensions import db
from app.models.enums import TipoSenha


class EstadoFila(db.Model):
    """Tabela de UMA linha só (id=1). Guarda o último tipo chamado para a
    alternância [SP] -> [SE|SG] e serve de ponto de bloqueio da concorrência."""

    __tablename__ = "estado_fila"

    id: Mapped[int] = mapped_column(primary_key=True)
    ultimo_tipo_chamado: Mapped[Optional[TipoSenha]] = mapped_column(Enum(TipoSenha))
    ultimo_nao_prioritario: Mapped[Optional[TipoSenha]] = mapped_column(Enum(TipoSenha))