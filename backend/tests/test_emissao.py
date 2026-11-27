from datetime import datetime

import pytest

from app.core.exceptions import ForaDoExpedienteError
from app.models import Senha, StatusSenha, TipoSenha
from app.services.emissao_service import EmissaoService, formatar_numero


def servico(hora, dia=9):
    return EmissaoService(agora=lambda: datetime(2026, 11, dia, hora, 0))


def test_formato_da_numeracao():
    assert formatar_numero(datetime(2026, 11, 9), TipoSenha.SP, 1) == "261109-SP001"
    assert formatar_numero(datetime(2026, 1, 5), TipoSenha.SE, 42) == "260105-SE042"


def test_emite_senha_aguardando(app):
    senha = servico(8).emitir(TipoSenha.SG)
    assert senha.numero_senha == "261109-SG001"
    assert senha.status_atual == StatusSenha.AGUARDANDO


def test_sequencial_por_tipo(app):
    s = servico(8)
    assert s.emitir(TipoSenha.SP).sequencial_diario == 1
    assert s.emitir(TipoSenha.SP).sequencial_diario == 2
    assert s.emitir(TipoSenha.SG).sequencial_diario == 1  # outro tipo recomeça


def test_sequencial_reinicia_no_dia_seguinte(app):
    servico(8, dia=9).emitir(TipoSenha.SP)
    senha = servico(8, dia=10).emitir(TipoSenha.SP)
    assert senha.numero_senha == "261110-SP001"


@pytest.mark.parametrize("hora", [6, 17, 22])
def test_bloqueia_fora_do_expediente(app, hora):
    with pytest.raises(ForaDoExpedienteError):
        servico(hora).emitir(TipoSenha.SG)
    assert Senha.query.count() == 0


def test_endpoint_rejeita_tipo_invalido(app):
    resp = app.test_client().post("/api/v1/senhas", json={"tipo": "XX"})
    assert resp.status_code == 422