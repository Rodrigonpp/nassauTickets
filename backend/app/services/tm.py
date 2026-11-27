import random

from app.models import TipoSenha


def duracao_simulada_min(tipo: TipoSenha, rng=random) -> float:
    if tipo == TipoSenha.SP:
        return rng.uniform(10, 20)       # 15 ± 5
    if tipo == TipoSenha.SG:
        return rng.uniform(2, 8)         # 5 ± 3
    return 1.0 if rng.random() < 0.95 else 5.0   # SE
