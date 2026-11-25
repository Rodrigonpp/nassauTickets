from datetime import datetime

import pytest

from app.core.exceptions import RegraNegocioError
from app.models import Perfil, Senha, TipoSenha, Usuario
from app.services.admin_service import AdminService
from app.services.emissao_service import EmissaoService


def test_descartar_sobras(app):
    EmissaoService(agora=lambda: datetime(2026, 11, 9, 8, 0)).emitir(TipoSenha.SG)
    assert AdminService().descartar_sobras() == 1
    assert Senha.query.first().motivo_descarte == "FIM_EXPEDIENTE"


def test_criar_usuario_e_rejeitar_duplicado(app):
    AdminService().criar_usuario(
        "Ana", "A9", "ana@nassau.com.br", "Senha@1234", "ATENDENTE"
    )
    usuario = Usuario.query.filter_by(login="ana@nassau.com.br").one()
    assert usuario.perfil == Perfil.ATENDENTE
    with pytest.raises(RegraNegocioError):
        AdminService().criar_usuario(
            "Ana2", "A9", "outra@nassau.com.br", "Senha@1234", "ATENDENTE"
        )


def test_admin_exige_gestor(app):
    r = app.test_client().post("/api/v1/admin/descartar-sobras")
    assert r.status_code in (401, 422)