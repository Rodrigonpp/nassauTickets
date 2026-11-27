from datetime import date, datetime

from app.models import TipoSenha
from app.services.atendimento_service import AtendimentoService
from app.services.chamada_service import ChamadaService
from app.services.emissao_service import EmissaoService
from app.services.relatorio_service import RelatorioService, intervalo_mes

DIA = date(2026, 11, 9)


def preparar():
    emissao = EmissaoService(agora=lambda: datetime(2026, 11, 9, 8, 0))
    for t in [TipoSenha.SP, TipoSenha.SG, TipoSenha.SG]:
        emissao.emitir(t)
    chamada = ChamadaService(agora=lambda: datetime(2026, 11, 9, 8, 10))
    atend = AtendimentoService(agora=lambda: datetime(2026, 11, 9, 8, 12))
    s1 = chamada.chamar_proximo(None, None)   # SP
    atend.iniciar(s1.id)
    atend.encerrar(s1.id)
    s2 = chamada.chamar_proximo(None, None)   # SG
    atend.chamar_novamente(s2.id)
    atend.nao_compareceu(s2.id)


def test_intervalo_mes():
    assert intervalo_mes("2026-11") == (date(2026, 11, 1), date(2026, 11, 30))


def test_resumo(app):
    preparar()
    r = RelatorioService().resumo(DIA, DIA)
    assert r["total_emitidas"] == 3
    assert r["total_atendidas"] == 1
    assert r["emitidas_por_tipo"] == {"SP": 1, "SG": 2, "SE": 0}
    assert r["atendidas_por_tipo"] == {"SP": 1, "SG": 0, "SE": 0}


def test_detalhado_deixa_campos_em_branco_se_nao_atendida(app):
    preparar()
    itens = {i["numero_senha"]: i for i in RelatorioService().detalhado(DIA, DIA)}
    assert itens["261109-SP001"]["atendida_em"] is not None
    assert itens["261109-SG001"]["atendida_em"] is None
    assert itens["261109-SG001"]["guiche"] is None


def test_tm_e_indicadores(app):
    preparar()
    tm = RelatorioService().tempo_medio(DIA, DIA)
    assert 10 <= tm["tm_minutos_por_tipo"]["SP"] <= 20
    ind = RelatorioService().indicadores(DIA, DIA)
    assert ind["taxa_nao_comparecimento_pct"] == 33.33
    assert ind["tempo_medio_espera_min"] == 10.0


def test_auditoria_traz_segunda_chamada(app):
    preparar()
    itens = RelatorioService().auditoria(DIA, DIA)
    assert len(itens) == 2
    assert any(i["segunda_chamada"] for i in itens)


def test_relatorio_exige_gestor(app):
    r = app.test_client().get("/api/v1/relatorios/resumo")
    assert r.status_code in (401, 422)