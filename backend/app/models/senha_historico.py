from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Enum, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from app.extensions import db
from app.models.enums import StatusSenha


class SenhaHistorico(db.Model):
    """Cada mudança de estado da senha vira uma linha (critério 2 do edital)."""

    __tablename__ = "senha_historico"

    id: Mapped[int] = mapped_column(primary_key=True)
    senha_id: Mapped[int] = mapped_column(
        ForeignKey("senhas.id"), nullable=False, index=True
    )
    status_anterior: Mapped[Optional[StatusSenha]] = mapped_column(Enum(StatusSenha))
    status_novo: Mapped[StatusSenha] = mapped_column(Enum(StatusSenha), nullable=False)
    usuario_id: Mapped[Optional[int]] = mapped_column(ForeignKey("usuarios.id"))
    registrado_em: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )