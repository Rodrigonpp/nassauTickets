from app.core.exceptions import (
    AtendenteOcupadoError,
    FilaVaziaError,
    ForaDoExpedienteError,
)
from app.extensions import db
from app.models import AtendimentoAuditoria, Senha, StatusSenha, TipoSenha
from app.repositories.fila_repository import FilaRepository
from app.services import relogio
from app.services.maquina_estados import transitar

T = TipoSenha

ORDEM_APOS_SP = [T.SE, T.SG, T.SP]       # última foi SP: vez de SE|SG
ORDEM_APOS_OUTRA = [T.SP, T.SE, T.SG]    # última foi SE/SG (ou início): vez de SP


def ordem_de_busca(ultimo: TipoSenha | None) -> list[TipoSenha]:
    return ORDEM_APOS_SP if ultimo == T.SP else ORDEM_APOS_OUTRA


class ChamadaService:
    def __init__(self, repo: FilaRepository | None = None, agora=None):
        self.repo = repo or FilaRepository()
        self.agora = agora or relogio.agora

    def chamar_proximo(self, usuario_id, guiche_id) -> Senha:
        if not relogio.dentro_do_expediente(self.agora()):
            raise ForaDoExpedienteError(
                "Fora do expediente: chamadas das 07h às 17h."
            )

        try:
            estado = self.repo.travar_estado_fila()

            if usuario_id is not None:
                em_andamento = (
                    db.session.query(AtendimentoAuditoria)
                    .join(Senha, Senha.id == AtendimentoAuditoria.senha_id)
                    .filter(
                        AtendimentoAuditoria.usuario_id == usuario_id,
                        Senha.status_atual.in_([
                            StatusSenha.CHAMADA,
                            StatusSenha.CHAMADA_NOVAMENTE,
                            StatusSenha.EM_ATENDIMENTO,
                        ]),
                    )
                    .first()
                )
                if em_andamento:
                    raise AtendenteOcupadoError(
                        "Finalize o atendimento atual antes de chamar outra senha."
                    )

            senha = None
            for tipo in ordem_de_busca(estado.ultimo_tipo_chamado):
                senha = self.repo.proxima_aguardando(tipo)
                if senha:
                    break
            if senha is None:
                raise FilaVaziaError("Não há senhas aguardando.")

            transitar(senha, StatusSenha.CHAMADA, usuario_id)
            db.session.add(
                AtendimentoAuditoria(
                    senha_id=senha.id,
                    usuario_id=usuario_id,
                    guiche_id=guiche_id,
                    horario_primeira_chamada=self.agora(),
                )
            )
            estado.ultimo_tipo_chamado = senha.tipo_senha
            if senha.tipo_senha != T.SP:
                estado.ultimo_nao_prioritario = senha.tipo_senha

            db.session.commit()  # libera o lock
            return senha
        except Exception:
            db.session.rollback()
            raise