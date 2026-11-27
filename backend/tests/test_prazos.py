from datetime import datetime, timedelta

from app.models import AtendimentoAuditoria, StatusSenha, TipoSenha
from app.services.atendimento_service import AtendimentoService
from app.services.chamada_service import ChamadaService
from app.services.emissao_service import EmissaoService

T0 = datetime(2026, 11, 9, 8, 5, 0)  # hora da 1ª chamada


def _chamar_uma_senha():
    EmissaoService(agora=lambda: datetime(2026, 11, 9, 8, 0)).emitir(TipoSenha.SG)
    return ChamadaService(agora=lambda: T0).chamar_proximo(None, None)


def _processar(segundos_depois):
    agora = T0 + timedelta(seconds=segundos_depois)
    return AtendimentoService(agora=lambda: agora).processar_prazos()


def test_antes_de_1_minuto_nada_muda(app):
    senha = _chamar_uma_senha()
    assert _processar(59) == 0
    assert senha.status_atual == StatusSenha.CHAMADA


def test_apos_1_minuto_a_senha_e_chamada_novamente(app):
    senha = _chamar_uma_senha()
    assert _processar(60) == 1
    assert senha.status_atual == StatusSenha.CHAMADA_NOVAMENTE


def test_apos_mais_1_minuto_a_senha_expira(app):
    senha = _chamar_uma_senha()
    _processar(60)
    assert _processar(119) == 0
    assert senha.status_atual == StatusSenha.CHAMADA_NOVAMENTE
    assert _processar(120) == 1
    assert senha.status_atual == StatusSenha.NAO_COMPARECEU


def test_rotina_atrasada_grava_a_hora_do_vencimento(app):
    senha = _chamar_uma_senha()
    assert _processar(300) == 2  # CHAMADA -> CHAMADA_NOVAMENTE -> NAO_COMPARECEU
    assert senha.status_atual == StatusSenha.NAO_COMPARECEU
    aud = AtendimentoAuditoria.query.filter_by(senha_id=senha.id).one()
    assert aud.horario_segunda_chamada == T0 + timedelta(seconds=60)


def test_senha_em_atendimento_nao_expira(app):
    senha = _chamar_uma_senha()
    AtendimentoService(agora=lambda: T0 + timedelta(seconds=30)).iniciar(senha.id)
    assert _processar(3600) == 0
    assert senha.status_atual == StatusSenha.EM_ATENDIMENTO