from argon2 import PasswordHasher

from app import create_app
from app.extensions import db
from app.models import EstadoFila, Guiche, Perfil, Usuario

ph = PasswordHasher()


def seed():
    app = create_app()
    with app.app_context():
        if Usuario.query.first():
            print("Seed já aplicado. Nada a fazer.")
            return

        db.session.add_all([
            Usuario(nome="Gestor Teste", matricula="G001", login="gestor",
                    senha_hash=ph.hash("Gestor@123"), perfil=Perfil.GESTOR),
            Usuario(nome="Atendente Um", matricula="A001", login="atendente1",
                    senha_hash=ph.hash("Atend@123"), perfil=Perfil.ATENDENTE),
            Usuario(nome="Atendente Dois", matricula="A002", login="atendente2",
                    senha_hash=ph.hash("Atend@123"), perfil=Perfil.ATENDENTE),
            Guiche(numero_guiche=1),
            Guiche(numero_guiche=2),
            Guiche(numero_guiche=3),
            EstadoFila(id=1),
        ])
        db.session.commit()
        print("Seed aplicado com sucesso.")


if __name__ == "__main__":
    seed()