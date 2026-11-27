from datetime import datetime

import pytest

from app.core.exceptions import TransicaoInvalidaError
from app.models import AtendimentoAuditoria, StatusSenha, TipoSenha
from app.services.atendimento_service import AtendimentoService
from app.services.chamada_service import ChamadaService
from app.services.emissao_service import EmissaoService

S = StatusSenha
AGORA = lambda: datetime(2026, 11, 9, 8, 10)


def senha_chamada():
    EmissaoService(agora=lambda: datetime(2026, 11, 9, 8, 0)).emitir(TipoSenha.SG)
    return ChamadaService(agora=AGORA).chamar_proximo(None, None)


def test_fluxo_completo(app):
    senha = senha_chamada()
    svc = AtendimentoService(agora=AGORA)
    svc.iniciar(senha.id)
    svc.encerrar(senha.id)
    assert senha.status_atual == S.ATENDIDA
    aud = AtendimentoAuditoria.query.filter_by(senha_id=senha.id).one()
    assert aud.horario_inicio_atendimento and aud.horario_finalizacao_atendimento


def test_duas_chamadas_e_nao_comparecimento(app):
    senha = senha_chamada()
    svc = AtendimentoService(agora=AGORA)
    svc.chamar_novamente(senha.id)
    svc.nao_compareceu(senha.id)
    assert senha.status_atual == S.NAO_COMPARECEU
    aud = AtendimentoAuditoria.query.filter_by(senha_id=senha.id).one()
    assert aud.horario_segunda_chamada is not None


def test_rejeita_encerrar_sem_iniciar(app):
    senha = senha_chamada()
    with pytest.raises(TransicaoInvalidaError):
        AtendimentoService(agora=AGORA).encerrar(senha.id)


def test_rejeita_nao_comparecer_com_uma_chamada(app):
    senha = senha_chamada()
    with pytest.raises(TransicaoInvalidaError):
        AtendimentoService(agora=AGORA).nao_compareceu(senha.id)