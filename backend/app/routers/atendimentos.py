from flask_smorest import Blueprint

from app.core.seguranca import perfil_requerido, usuario_atual_id
from app.schemas.senha_schema import (
    ChamarSchema,
    EstadoAtendenteSchema,
    SenhaSchema,
)
from app.services.atendimento_service import AtendimentoService
from app.services.chamada_service import ChamadaService
from app.services.estado_atendente_service import EstadoAtendenteService

blp = Blueprint(
    "atendimentos", __name__, url_prefix="/api/v1/atendimentos",
    description="Chamada e atendimento (requer login de ATENDENTE)",
)

SEGURANCA = [{"bearerAuth": []}]


@blp.before_request
def aplicar_prazos():
    """Antes de qualquer ação, expira/rechama as senhas que passaram do prazo."""
    AtendimentoService().processar_prazos()


@blp.route("/chamar-proximo", methods=["POST"])
@blp.arguments(ChamarSchema)
@blp.response(200, SenhaSchema)
@blp.doc(security=SEGURANCA)
@perfil_requerido("ATENDENTE")
def chamar_proximo(dados):
    """Chama a próxima senha seguindo a alternância SP -> SE|SG."""
    return ChamadaService().chamar_proximo(usuario_atual_id(), dados["guiche_id"])


@blp.route("/<int:senha_id>/chamar-novamente", methods=["POST"])
@blp.response(200, SenhaSchema)
@blp.doc(security=SEGURANCA)
@perfil_requerido("ATENDENTE")
def chamar_novamente(senha_id):
    """Segunda chamada (última antes do não comparecimento)."""
    return AtendimentoService().chamar_novamente(senha_id, usuario_atual_id())


@blp.route("/<int:senha_id>/iniciar", methods=["POST"])
@blp.response(200, SenhaSchema)
@blp.doc(security=SEGURANCA)
@perfil_requerido("ATENDENTE")
def iniciar(senha_id):
    """Cliente chegou ao guichê: inicia o atendimento."""
    return AtendimentoService().iniciar(senha_id, usuario_atual_id())


@blp.route("/<int:senha_id>/encerrar", methods=["POST"])
@blp.response(200, SenhaSchema)
@blp.doc(security=SEGURANCA)
@perfil_requerido("ATENDENTE")
def encerrar(senha_id):
    """Finaliza o atendimento."""
    return AtendimentoService().encerrar(senha_id, usuario_atual_id())


@blp.route("/<int:senha_id>/nao-compareceu", methods=["POST"])
@blp.response(200, SenhaSchema)
@blp.doc(security=SEGURANCA)
@perfil_requerido("ATENDENTE")
def nao_compareceu(senha_id):
    """Cliente não compareceu após as duas chamadas."""
    return AtendimentoService().nao_compareceu(senha_id, usuario_atual_id())


@blp.route("/estado", methods=["GET"])
@blp.response(200, EstadoAtendenteSchema)
@blp.doc(security=SEGURANCA)
@perfil_requerido("ATENDENTE")
def estado():
    """Fila por tipo, senha em andamento do atendente e últimas chamadas."""
    return EstadoAtendenteService().obter(usuario_atual_id())