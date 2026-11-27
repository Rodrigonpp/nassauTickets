from app.core.exceptions import TransicaoInvalidaError
from app.extensions import db
from app.models import Senha, SenhaHistorico, StatusSenha

S = StatusSenha

TRANSICOES_PERMITIDAS = {
    S.EMITIDA: {S.AGUARDANDO},
    S.AGUARDANDO: {S.CHAMADA},
    S.CHAMADA: {S.CHAMADA_NOVAMENTE, S.EM_ATENDIMENTO},
    S.CHAMADA_NOVAMENTE: {S.EM_ATENDIMENTO, S.NAO_COMPARECEU},
    S.EM_ATENDIMENTO: {S.ATENDIDA},
    S.ATENDIDA: set(),
    S.NAO_COMPARECEU: set(),
}


def pode_transitar(atual: StatusSenha, novo: StatusSenha) -> bool:
    return novo in TRANSICOES_PERMITIDAS[atual]


def transitar(senha: Senha, novo: StatusSenha, usuario_id: int | None = None) -> None:
    """Muda o estado da senha, valida a transição e grava o histórico.

    Não faz commit: quem chama controla a transação, para que a mudança de
    estado e as demais alterações (auditoria, guichê) sejam atômicas.
    """
    atual = senha.status_atual
    if not pode_transitar(atual, novo):
        raise TransicaoInvalidaError(
            f"Transição inválida: {atual.value} -> {novo.value}"
        )

    senha.status_atual = novo
    db.session.add(
        SenhaHistorico(
            senha_id=senha.id,
            status_anterior=atual,
            status_novo=novo,
            usuario_id=usuario_id,
        )
    )