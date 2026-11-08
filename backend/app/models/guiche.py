from typing import Optional

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.extensions import db
from app.models.enums import StatusGuiche


class Guiche(db.Model):
    __tablename__ = "guiches"

    id: Mapped[int] = mapped_column(primary_key=True)
    numero_guiche: Mapped[int] = mapped_column(unique=True, nullable=False)
    status: Mapped[StatusGuiche] = mapped_column(
        Enum(StatusGuiche), default=StatusGuiche.DISPONIVEL, nullable=False
    )
    # Atendente que está usando o guichê agora (null = ninguém)
    usuario_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("usuarios.id"), nullable=True
    )