from datetime import datetime

import pytest

from app.core.exceptions import FilaVaziaError
from app.models import TipoSenha
from app.services.chamada_service import ChamadaService, ordem_de_busca
from app.services.emissao_service import EmissaoService

T = TipoSenha


def emitir(tipos):
    svc = EmissaoService(agora=lambda: datetime(2026, 11, 9, 8, 0))
    for t in tipos:
        svc.emitir(t)


def chamar_tudo(n):
    svc = ChamadaService(agora=lambda: datetime(2026, 11, 9, 8, 5))
    return [svc.chamar_proximo(None, None).numero_senha for _ in range(n)]


def test_ordem_de_busca():
    assert ordem_de_busca(None) == [T.SP, T.SE, T.SG]
    assert ordem_de_busca(T.SP) == [T.SE, T.SG, T.SP]
    assert ordem_de_busca(T.SE) == [T.SP, T.SE, T.SG]
    assert ordem_de_busca(T.SG) == [T.SP, T.SE, T.SG]


def test_alternancia_sp_depois_se_sg(app):
    emitir([T.SG, T.SG, T.SE, T.SP, T.SP, T.SE])
    assert chamar_tudo(6) == [
        "261109-SP001",
        "261109-SE001",
        "261109-SP002",
        "261109-SE002",
        "261109-SG001",
        "261109-SG002",
    ]


def test_fila_so_com_sg(app):
    emitir([T.SG, T.SG])
    assert chamar_tudo(2) == ["261109-SG001", "261109-SG002"]


def test_fila_vazia(app):
    with pytest.raises(FilaVaziaError):
        ChamadaService().chamar_proximo(None, None)