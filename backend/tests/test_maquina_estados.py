from datetime import date, datetime

import pytest

from app.core.exceptions import TransicaoInvalidaError
from app.models import Senha, SenhaHistorico, StatusSenha, TipoSenha
from app.services.maquina_estados import transitar

S = StatusSenha


def criar_senha(db):
    senha = Senha(
        numero_senha="261109-SP001",
        tipo_senha=TipoSenha.SP,
        sequencial_diario=1,
        data_emissao=date(2026, 11, 9),
        data_hora_emissao=datetime(2026, 11, 9, 8, 0),
    )
    db.session.add(senha)
    db.session.commit()
    return senha


def test_fluxo_completo_valido(db):
    senha = criar_senha(db)
    for novo in [S.AGUARDANDO, S.CHAMADA, S.EM_ATENDIMENTO, S.ATENDIDA]:
        transitar(senha, novo)
    db.session.commit()

    assert senha.status_atual == S.ATENDIDA
    assert SenhaHistorico.query.filter_by(senha_id=senha.id).count() == 4


def test_fluxo_nao_comparecimento(db):
    senha = criar_senha(db)
    for novo in [S.AGUARDANDO, S.CHAMADA, S.CHAMADA_NOVAMENTE, S.NAO_COMPARECEU]:
        transitar(senha, novo)
    db.session.commit()
    assert senha.status_atual == S.NAO_COMPARECEU


def test_rejeita_pular_estado(db):
    senha = criar_senha(db)
    with pytest.raises(TransicaoInvalidaError):
        transitar(senha, S.EM_ATENDIMENTO)  # EMITIDA -> EM_ATENDIMENTO


def test_estados_finais_nao_saem(db):
    senha = criar_senha(db)
    for novo in [S.AGUARDANDO, S.CHAMADA, S.EM_ATENDIMENTO, S.ATENDIDA]:
        transitar(senha, novo)
    with pytest.raises(TransicaoInvalidaError):
        transitar(senha, S.AGUARDANDO)


def test_transicao_invalida_nao_grava_historico(db):
    senha = criar_senha(db)
    with pytest.raises(TransicaoInvalidaError):
        transitar(senha, S.ATENDIDA)
    assert SenhaHistorico.query.count() == 0