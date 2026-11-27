from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.extensions import db


class AtendimentoAuditoria(db.Model):
    __tablename__ = "atendimentos_auditoria"

    id: Mapped[int] = mapped_column(primary_key=True)
    # unique=True: uma senha só pode ter UM atendimento (trava duplicidade)
    senha_id: Mapped[int] = mapped_column(
        ForeignKey("senhas.id"), unique=True, nullable=False
    )
    usuario_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("usuarios.id"), nullable=True, index=True
    )
    guiche_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("guiches.id"), nullable=True, index=True
    )
    horario_primeira_chamada: Mapped[Optional[datetime]] = mapped_column(DateTime)
    horario_segunda_chamada: Mapped[Optional[datetime]] = mapped_column(DateTime)
    horario_inicio_atendimento: Mapped[Optional[datetime]] = mapped_column(DateTime)
    horario_finalizacao_atendimento: Mapped[Optional[datetime]] = mapped_column(DateTime)