from flask_smorest import Blueprint

from app.models import TipoSenha
from app.schemas.senha_schema import EmitirSenhaSchema, SenhaSchema
from app.services.emissao_service import EmissaoService

blp = Blueprint(
    "senhas", __name__, url_prefix="/api/v1/senhas", description="Totem e fila"
)


@blp.route("", methods=["POST"])
@blp.arguments(EmitirSenhaSchema)
@blp.response(201, SenhaSchema)
def emitir_senha(dados):
    """Emite uma senha (SP, SG ou SE). Anônimo: chamado apenas pelo totem."""
    return EmissaoService().emitir(TipoSenha(dados["tipo"]))