from flask_smorest import Blueprint

from app.schemas.senha_schema import AcaoSenhaSchema, ChamarSchema, SenhaSchema
from app.services.atendimento_service import AtendimentoService
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


@blp.route("/<int:senha_id>/chamar-novamente", methods=["POST"])
@blp.arguments(AcaoSenhaSchema)
@blp.response(200, SenhaSchema)
def chamar_novamente(dados, senha_id):
    """Segunda chamada da senha (a última antes de marcar não comparecimento)."""
    return AtendimentoService().chamar_novamente(senha_id, dados["usuario_id"])


@blp.route("/<int:senha_id>/iniciar", methods=["POST"])
@blp.arguments(AcaoSenhaSchema)
@blp.response(200, SenhaSchema)
def iniciar(dados, senha_id):
    """Cliente chegou ao guichê: inicia o atendimento."""
    return AtendimentoService().iniciar(senha_id, dados["usuario_id"])


@blp.route("/<int:senha_id>/encerrar", methods=["POST"])
@blp.arguments(AcaoSenhaSchema)
@blp.response(200, SenhaSchema)
def encerrar(dados, senha_id):
    """Finaliza o atendimento."""
    return AtendimentoService().encerrar(senha_id, dados["usuario_id"])


@blp.route("/<int:senha_id>/nao-compareceu", methods=["POST"])
@blp.arguments(AcaoSenhaSchema)
@blp.response(200, SenhaSchema)
def nao_compareceu(dados, senha_id):
    """Cliente não compareceu após as duas chamadas."""
    return AtendimentoService().nao_compareceu(senha_id, dados["usuario_id"])