from datetime import datetime

from app.models import TipoSenha
from app.services.atendimento_service import AtendimentoService
from app.services.chamada_service import ChamadaService
from app.services.emissao_service import EmissaoService
from app.services.painel_service import PainelService


def test_painel_mostra_so_as_5_ultimas_chamadas(app):
    emissao = EmissaoService(agora=lambda: datetime(2026, 11, 9, 8, 0))
    for _ in range(7):
        emissao.emitir(TipoSenha.SG)
    chamada = ChamadaService(agora=lambda: datetime(2026, 11, 9, 8, 5))
    for _ in range(6):
        chamada.chamar_proximo(None, None)

    itens = PainelService().ultimas_chamadas()
    assert len(itens) == 5
    assert itens[0]["numero_senha"] == "261109-SG006"      # a mais recente
    assert all(i["numero_senha"] != "261109-SG007" for i in itens)  # nunca a próxima


def test_ultima_chamada_marcada_apos_rechamar(app):
    EmissaoService(agora=lambda: datetime(2026, 11, 9, 8, 0)).emitir(TipoSenha.SG)
    senha = ChamadaService(agora=lambda: datetime(2026, 11, 9, 8, 5)).chamar_proximo(None, None)
    assert PainelService().ultimas_chamadas()[0]["ultima_chamada"] is False
    AtendimentoService(agora=lambda: datetime(2026, 11, 9, 8, 7)).chamar_novamente(senha.id)
    assert PainelService().ultimas_chamadas()[0]["ultima_chamada"] is True