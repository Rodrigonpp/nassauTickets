from marshmallow import Schema, fields


class PainelItemSchema(Schema):
    numero_senha = fields.String()
    tipo_senha = fields.String()
    sequencial = fields.Integer()
    guiche = fields.Integer(allow_none=True)
    ultima_chamada = fields.Boolean()
    chamada_em = fields.DateTime()