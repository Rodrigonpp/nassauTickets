import pytest
from argon2 import PasswordHasher

from app.extensions import db
from app.models import LogAcesso, Perfil, Usuario

ph = PasswordHasher()


@pytest.fixture()
def usuarios(app):
    db.session.add_all([
        Usuario(nome="Gestor", matricula="G1", login="gestor",
                senha_hash=ph.hash("Gestor@123"), perfil=Perfil.GESTOR),
        Usuario(nome="Atend", matricula="A1", login="atend",
                senha_hash=ph.hash("Atend@123"), perfil=Perfil.ATENDENTE),
    ])
    db.session.commit()


def login(client, user, senha):
    return client.post("/api/v1/auth/login", json={"login": user, "senha": senha})


def test_login_ok_devolve_token(app, usuarios):
    r = login(app.test_client(), "atend", "Atend@123")
    assert r.status_code == 200
    assert r.json["perfil"] == "ATENDENTE" and r.json["access_token"]


def test_login_senha_errada_401_e_log(app, usuarios):
    r = login(app.test_client(), "atend", "errada")
    assert r.status_code == 401
    assert LogAcesso.query.filter_by(acao="LOGIN_FALHA").count() == 1


def test_chamar_proximo_sem_token_401(app):
    r = app.test_client().post("/api/v1/atendimentos/chamar-proximo", json={"guiche_id": 1})
    assert r.status_code in (401, 422)


def test_gestor_nao_chama_senha_403(app, usuarios):
    c = app.test_client()
    token = login(c, "gestor", "Gestor@123").json["access_token"]
    r = c.post("/api/v1/atendimentos/chamar-proximo", json={"guiche_id": 1},
               headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 403