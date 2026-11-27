from app.models import TipoSenha
from app.services.tm import duracao_simulada_min


def test_faixas_do_tm():
    for _ in range(200):
        assert 10 <= duracao_simulada_min(TipoSenha.SP) <= 20
        assert 2 <= duracao_simulada_min(TipoSenha.SG) <= 8
        assert duracao_simulada_min(TipoSenha.SE) in (1.0, 5.0)