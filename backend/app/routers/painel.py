from flask_smorest import Blueprint

from app.schemas.painel_schema import PainelItemSchema
from app.services.atendimento_service import AtendimentoService
from app.services.painel_service import PainelService

blp = Blueprint(
    "painel", __name__, url_prefix="/api/v1/painel", description="Painel de chamadas"
)

@blp.before_request
def aplicar_prazos():
    """Antes de responder, expira/rechama as senhas que passaram do prazo."""
    AtendimentoService().processar_prazos()

@blp.route("", methods=["GET"])
@blp.response(200, PainelItemSchema(many=True))
def painel():
    """Últimas 5 senhas chamadas (nunca a próxima). Público: usado pelo painel."""
    return PainelService().ultimas_chamadas(5)