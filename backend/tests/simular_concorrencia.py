"""Chamadas simultâneas: prova que nenhuma senha sai duplicada.
Uso: python -m tests.simular_concorrencia
"""
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from app import create_app
from app.extensions import db
from app.models import AtendimentoAuditoria, EstadoFila, Senha, SenhaHistorico
from app.models import TipoSenha as T
from app.services.chamada_service import ChamadaService
from app.services.emissao_service import EmissaoService

app = create_app()
N_SENHAS = 30
N_ATENDENTES = 10


def limpar():
    db.session.query(AtendimentoAuditoria).delete()
    db.session.query(SenhaHistorico).delete()
    db.session.query(Senha).delete()
    estado = db.session.get(EstadoFila, 1)
    if estado:
        estado.ultimo_tipo_chamado = None
        estado.ultimo_nao_prioritario = None
    db.session.commit()


def chamar():
    with app.app_context():
        try:
            return ChamadaService().chamar_proximo(None, None).numero_senha
        except Exception as e:
            return f"ERRO:{type(e).__name__}"
        finally:
            db.session.remove()


with app.app_context():
    limpar()
    svc = EmissaoService(agora=lambda: datetime(2026, 11, 9, 8, 0))
    for i in range(N_SENHAS):
        svc.emitir([T.SP, T.SG, T.SE][i % 3])

with ThreadPoolExecutor(max_workers=N_ATENDENTES) as pool:
    resultados = list(pool.map(lambda _: chamar(), range(N_SENHAS)))

repetidas = [n for n, c in Counter(resultados).items() if c > 1]
erros = [r for r in resultados if r.startswith("ERRO")]
print(f"Chamadas: {len(resultados)} | únicas: {len(set(resultados))}")
print(f"Duplicadas: {repetidas or 'nenhuma'} | erros: {erros or 'nenhum'}")
print("RESULTADO:", "OK" if not repetidas and not erros else "FALHOU")