from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.extensions import db


class LogAcesso(db.Model):
    """Registro de acesso exigido pela LGPD (item 5.3 do edital)."""

    __tablename__ = "log_acesso"

    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("usuarios.id"), index=True
    )
    acao: Mapped[str] = mapped_column(String(60), nullable=False)
    ip: Mapped[Optional[str]] = mapped_column(String(45))
    registrado_em: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )