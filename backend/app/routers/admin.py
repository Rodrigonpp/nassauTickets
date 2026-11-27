from flask_smorest import Blueprint
from marshmallow import Schema, fields
from marshmallow.validate import Length, OneOf

from app.core.seguranca import perfil_requerido
from app.services.admin_service import AdminService

blp = Blueprint(
    "admin", __name__, url_prefix="/api/v1/admin",
    description="Administração (requer GESTOR)",
)
SEGURANCA = [{"bearerAuth": []}]


class NovoUsuarioSchema(Schema):
    nome = fields.String(required=True)
    matricula = fields.String(required=True)
    login = fields.String(required=True)
    senha = fields.String(required=True, load_only=True, validate=Length(min=8))
    perfil = fields.String(required=True, validate=OneOf(["ATENDENTE", "GESTOR"]))


class UsuarioSchema(Schema):
    id = fields.Integer()
    nome = fields.String()
    login = fields.String()
    perfil = fields.Function(lambda u: u.perfil.value)


@blp.route("/descartar-sobras", methods=["POST"])
@blp.doc(security=SEGURANCA)
@perfil_requerido("GESTOR")
def descartar_sobras():
    """Fim do expediente: descarta as senhas que sobraram aguardando."""
    return {"descartadas": AdminService().descartar_sobras()}


@blp.route("/usuarios", methods=["POST"])
@blp.arguments(NovoUsuarioSchema)
@blp.response(201, UsuarioSchema)
@blp.doc(security=SEGURANCA)
@perfil_requerido("GESTOR")
def criar_usuario(d):
    """Cadastra atendente ou gestor."""
    return AdminService().criar_usuario(
        d["nome"], d["matricula"], d["login"], d["senha"], d["perfil"]
    )