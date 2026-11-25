from datetime import date

from flask_smorest import Blueprint, abort
from marshmallow import Schema, fields

from app.core.seguranca import perfil_requerido
from app.services.relatorio_service import RelatorioService, intervalo_mes

blp = Blueprint(
    "relatorios", __name__, url_prefix="/api/v1/relatorios",
    description="Relatórios, auditoria e indicadores (requer GESTOR)",
)
SEGURANCA = [{"bearerAuth": []}]


class PeriodoSchema(Schema):
    data = fields.Date(metadata={"description": "Dia (AAAA-MM-DD). Relatório diário."})
    mes = fields.String(metadata={"description": "Mês (AAAA-MM). Relatório mensal."})


def _periodo(args):
    if args.get("mes"):
        try:
            return intervalo_mes(args["mes"])
        except (ValueError, IndexError):
            abort(422, message="Mês inválido. Use AAAA-MM.")
    dia = args.get("data") or date.today()
    return dia, dia


def _rota(caminho, metodo):
    def deco(fn):
        fn = perfil_requerido("GESTOR")(fn)
        fn = blp.doc(security=SEGURANCA)(fn)
        fn = blp.arguments(PeriodoSchema, location="query")(fn)
        return blp.route(caminho, methods=["GET"])(fn)
    return deco


@_rota("/resumo", "GET")
def resumo(args):
    """Quantitativo geral e por tipo (emitidas e atendidas)."""
    ini, fim = _periodo(args)
    return RelatorioService().resumo(ini, fim)


@_rota("/detalhado", "GET")
def detalhado(args):
    """Detalhe por senha: numeração, tipo, emissão, atendimento e guichê."""
    ini, fim = _periodo(args)
    return {"itens": RelatorioService().detalhado(ini, fim)}


@_rota("/tm", "GET")
def tm(args):
    """Tempo médio de atendimento por tipo."""
    ini, fim = _periodo(args)
    return RelatorioService().tempo_medio(ini, fim)


@_rota("/auditoria", "GET")
def auditoria(args):
    """AA, guichê, senha, 1ª/2ª chamada, início e fim."""
    ini, fim = _periodo(args)
    return {"itens": RelatorioService().auditoria(ini, fim)}


@_rota("/indicadores", "GET")
def indicadores(args):
    """Espera média, não comparecimento, descarte e produtividade."""
    ini, fim = _periodo(args)
    return RelatorioService().indicadores(ini, fim)