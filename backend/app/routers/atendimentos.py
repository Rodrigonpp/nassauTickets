from flask_smorest import Blueprint

from app.schemas.senha_schema import ChamarSchema, SenhaSchema
from app.services.chamada_service import ChamadaService

blp = Blueprint(
    "atendimentos", __name__, url_prefix="/api/v1/atendimentos",
    description="Chamada e atendimento",
)


@blp.route("/chamar-proximo", methods=["POST"])
@blp.arguments(ChamarSchema)
@blp.response(200, SenhaSchema)
def chamar_proximo(dados):
    """Chama a próxima senha seguindo a alternância SP -> SE|SG."""
    return ChamadaService().chamar_proximo(dados["usuario_id"], dados["guiche_id"])