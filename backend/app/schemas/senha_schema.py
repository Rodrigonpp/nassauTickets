from marshmallow import Schema, fields
from marshmallow.validate import OneOf

TIPOS = ["SP", "SG", "SE"]


class EmitirSenhaSchema(Schema):
    tipo = fields.String(required=True, validate=OneOf(TIPOS))


class SenhaSchema(Schema):
    numero_senha = fields.String()
    tipo_senha = fields.Function(lambda s: s.tipo_senha.value)
    status_atual = fields.Function(lambda s: s.status_atual.value)
    data_hora_emissao = fields.DateTime()

class ChamarSchema(Schema):
    usuario_id = fields.Integer(required=True)
    guiche_id = fields.Integer(required=True)

class AcaoSenhaSchema(Schema):
    usuario_id = fields.Integer(load_default=None)


class ChamadaDetalheSchema(SenhaSchema):
    id = fields.Integer()