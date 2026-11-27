from argon2 import PasswordHasher

from app import create_app
from app.extensions import db
from app.models import EstadoFila, Guiche, Perfil, Usuario

ph = PasswordHasher()
SENHA_ATENDENTE = "Atend@123"
SENHA_GESTOR = "Gestor@123"


def seed():
    app = create_app()
    with app.app_context():
        if Usuario.query.first():
            print("Seed já aplicado. Nada a fazer.")
            return

        usuarios = [
            Usuario(nome="Gestor", matricula="G001",
                    login="gestor@nassau.com.br",
                    senha_hash=ph.hash(SENHA_GESTOR), perfil=Perfil.GESTOR)
        ]
        hash_atendente = ph.hash(SENHA_ATENDENTE)  # um hash só: seed mais rápido
        for i in range(1, 11):
            usuarios.append(
                Usuario(nome=f"Atendente {i}", matricula=f"A{i:03d}",
                        login=f"usuario{i}@nassau.com.br",
                        senha_hash=hash_atendente, perfil=Perfil.ATENDENTE)
            )

        db.session.add_all(usuarios)
        db.session.add_all([Guiche(numero_guiche=n) for n in range(1, 11)])
        db.session.add(EstadoFila(id=1))
        db.session.commit()
        print("Seed aplicado: 1 gestor, 10 atendentes e 10 guichês.")


if __name__ == "__main__":
    seed()