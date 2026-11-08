from datetime import datetime
from typing import Callable

from sqlalchemy.exc import IntegrityError

from app.core.exceptions import ForaDoExpedienteError, RegraNegocioError
from app.extensions import db
from app.models import Senha, StatusSenha, TipoSenha
from app.repositories.senha_repository import SenhaRepository
from app.services import relogio
from app.services.maquina_estados import transitar

MAX_TENTATIVAS = 5
SEQUENCIAL_MAXIMO = 999  # SQ tem 3 dígitos no formato YYMMDD-PPSQ


def formatar_numero(momento: datetime, tipo: TipoSenha, sequencial: int) -> str:
    return f"{momento:%y%m%d}-{tipo.value}{sequencial:03d}"


class EmissaoService:
    def __init__(
        self,
        repo: SenhaRepository | None = None,
        agora: Callable[[], datetime] | None = None,
    ):
        self.repo = repo or SenhaRepository()
        self.agora = agora or relogio.agora

    def emitir(self, tipo: TipoSenha) -> Senha:
        momento = self.agora()
        if not relogio.dentro_do_expediente(momento):
            raise ForaDoExpedienteError(
                "Fora do expediente: emissão de senhas das 07h às 17h."
            )

        for _ in range(MAX_TENTATIVAS):
            sequencial = self.repo.proximo_sequencial(momento.date(), tipo)
            if sequencial > SEQUENCIAL_MAXIMO:
                raise RegraNegocioError(
                    f"Limite diário de senhas {tipo.value} atingido."
                )

            senha = Senha(
                numero_senha=formatar_numero(momento, tipo, sequencial),
                tipo_senha=tipo,
                sequencial_diario=sequencial,
                data_emissao=momento.date(),
                data_hora_emissao=momento,
                status_atual=StatusSenha.EMITIDA,
            )
            try:
                self.repo.adicionar(senha)
                db.session.flush()  # força o INSERT: colisão aparece aqui
                transitar(senha, StatusSenha.AGUARDANDO)
                db.session.commit()
                return senha
            except IntegrityError:
                db.session.rollback()  # outro totem pegou o número: tenta de novo

        raise RegraNegocioError("Não foi possível emitir a senha. Tente novamente.")