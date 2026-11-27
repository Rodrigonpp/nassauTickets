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
   
    guiche_id = fields.Integer(required=True)

class AcaoSenhaSchema(Schema):
    usuario_id = fields.Integer(load_default=None)


class ChamadaDetalheSchema(SenhaSchema):
    id = fields.Integer()

class SenhaEstadoSchema(Schema):
    id = fields.Integer()
    numero_senha = fields.String()
    tipo_senha = fields.String()
    status_atual = fields.String()
    data_hora_emissao = fields.DateTime()
    primeira_chamada_em = fields.DateTime(allow_none=True)
    ultima_chamada_em = fields.DateTime(allow_none=True)
    prazo_segundos = fields.Integer(allow_none=True)
    segundos_restantes = fields.Integer(allow_none=True)


class EstadoAtendenteSchema(Schema):
    fila = fields.Dict(keys=fields.String(), values=fields.Integer())
    atual = fields.Nested(SenhaEstadoSchema, allow_none=True)
    ultimas = fields.List(fields.Nested(SenhaEstadoSchema))