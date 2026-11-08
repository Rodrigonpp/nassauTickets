from datetime import date, datetime
from typing import Optional

from sqlalchemy import Date, DateTime, Enum, Index, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.extensions import db
from app.models.enums import StatusSenha, TipoSenha


class Senha(db.Model):
    __tablename__ = "senhas"
    __table_args__ = (
        # Garante que o sequencial nunca se repita no mesmo dia e tipo
        UniqueConstraint(
            "data_emissao", "tipo_senha", "sequencial_diario", name="uq_senha_dia_tipo_seq"
        ),
        # Acelera a busca da próxima senha da fila (consulta mais frequente)
        Index("ix_senhas_fila", "status_atual", "tipo_senha", "data_hora_emissao"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    numero_senha: Mapped[str] = mapped_column(String(15), unique=True, nullable=False)
    tipo_senha: Mapped[TipoSenha] = mapped_column(Enum(TipoSenha), nullable=False)
    sequencial_diario: Mapped[int] = mapped_column(nullable=False)
    data_emissao: Mapped[date] = mapped_column(Date, nullable=False)
    status_atual: Mapped[StatusSenha] = mapped_column(
        Enum(StatusSenha), default=StatusSenha.EMITIDA, nullable=False
    )
    data_hora_emissao: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    descartada_em: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    motivo_descarte: Mapped[Optional[str]] = mapped_column(String(60), nullable=True)