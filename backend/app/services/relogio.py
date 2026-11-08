from datetime import datetime
from zoneinfo import ZoneInfo

from flask import current_app


def agora() -> datetime:
    """Hora atual no fuso do laboratório, sem tzinfo (o banco guarda naive)."""
    fuso = ZoneInfo(current_app.config["FUSO_HORARIO"])
    return datetime.now(fuso).replace(tzinfo=None, microsecond=0)


def dentro_do_expediente(momento: datetime) -> bool:
    inicio = current_app.config["EXPEDIENTE_INICIO"]
    fim = current_app.config["EXPEDIENTE_FIM"]
    return inicio <= momento.hour < fim
