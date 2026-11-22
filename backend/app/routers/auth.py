from flask import request
from flask_smorest import Blueprint
from marshmallow import Schema, fields

from app.services.auth_service import AuthService

blp = Blueprint("auth", __name__, url_prefix="/api/v1/auth", description="Autenticação")


class LoginSchema(Schema):
    login = fields.String(required=True)
    senha = fields.String(required=True, load_only=True)


class TokenSchema(Schema):
    access_token = fields.String()
    perfil = fields.String()
    nome = fields.String()
    usuario_id = fields.Integer()


@blp.route("/login", methods=["POST"])
@blp.arguments(LoginSchema)
@blp.response(200, TokenSchema)
def login(dados):
    """Login de atendente ou gestor. Devolve o token JWT."""
    return AuthService().login(dados["login"], dados["senha"], request.remote_addr)