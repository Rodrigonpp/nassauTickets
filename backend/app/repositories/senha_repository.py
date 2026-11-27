from datetime import date

from sqlalchemy import func

from app.extensions import db
from app.models import Senha, TipoSenha


class SenhaRepository:
    def proximo_sequencial(self, dia: date, tipo: TipoSenha) -> int:
        maior = (
            db.session.query(func.max(Senha.sequencial_diario))
            .filter(Senha.data_emissao == dia, Senha.tipo_senha == tipo)
            .scalar()
        )
        return (maior or 0) + 1

    def adicionar(self, senha: Senha) -> None:
        db.session.add(senha)