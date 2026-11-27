from calendar import monthrange
from datetime import date

from sqlalchemy import select

from app.extensions import db
from app.models import AtendimentoAuditoria, Guiche, Senha, StatusSenha, TipoSenha, Usuario


def intervalo_mes(mes: str) -> tuple[date, date]:
    ano, m = (int(x) for x in mes.split("-"))
    return date(ano, m, 1), date(ano, m, monthrange(ano, m)[1])


class RelatorioService:
    def _senhas(self, ini: date, fim: date):
        return db.session.execute(
            select(Senha)
            .where(Senha.data_emissao >= ini, Senha.data_emissao <= fim)
            .order_by(Senha.data_hora_emissao, Senha.id)
        ).scalars().all()

    def resumo(self, ini: date, fim: date) -> dict:
        senhas = self._senhas(ini, fim)
        emitidas = {t.value: 0 for t in TipoSenha}
        atendidas = {t.value: 0 for t in TipoSenha}
        for s in senhas:
            emitidas[s.tipo_senha.value] += 1
            if s.status_atual == StatusSenha.ATENDIDA:
                atendidas[s.tipo_senha.value] += 1
        return {
            "periodo": {"inicio": ini.isoformat(), "fim": fim.isoformat()},
            "total_emitidas": len(senhas),
            "total_atendidas": sum(atendidas.values()),
            "emitidas_por_tipo": emitidas,
            "atendidas_por_tipo": atendidas,
        }

    def detalhado(self, ini: date, fim: date) -> list[dict]:
        linhas = db.session.execute(
            select(Senha, AtendimentoAuditoria, Guiche)
            .outerjoin(AtendimentoAuditoria, AtendimentoAuditoria.senha_id == Senha.id)
            .outerjoin(Guiche, Guiche.id == AtendimentoAuditoria.guiche_id)
            .where(Senha.data_emissao >= ini, Senha.data_emissao <= fim)
            .order_by(Senha.data_hora_emissao, Senha.id)
        ).all()
        itens = []
        for senha, aud, guiche in linhas:
            atendida = senha.status_atual == StatusSenha.ATENDIDA
            itens.append({
                "numero_senha": senha.numero_senha,
                "tipo_senha": senha.tipo_senha.value,
                "status": senha.status_atual.value,
                "emitida_em": senha.data_hora_emissao,
                # campos de atendimento ficam em branco se não atendida
                "atendida_em": aud.horario_inicio_atendimento if atendida and aud else None,
                "guiche": guiche.numero_guiche if atendida and guiche else None,
            })
        return itens

    def tempo_medio(self, ini: date, fim: date) -> dict:
        linhas = db.session.execute(
            select(Senha.tipo_senha, AtendimentoAuditoria)
            .join(AtendimentoAuditoria, AtendimentoAuditoria.senha_id == Senha.id)
            .where(
                Senha.data_emissao >= ini, Senha.data_emissao <= fim,
                AtendimentoAuditoria.horario_inicio_atendimento.is_not(None),
                AtendimentoAuditoria.horario_finalizacao_atendimento.is_not(None),
            )
        ).all()
        soma = {t.value: 0.0 for t in TipoSenha}
        qtd = {t.value: 0 for t in TipoSenha}
        for tipo, aud in linhas:
            dur = (aud.horario_finalizacao_atendimento
                   - aud.horario_inicio_atendimento).total_seconds() / 60
            soma[tipo.value] += dur
            qtd[tipo.value] += 1
        return {
            "periodo": {"inicio": ini.isoformat(), "fim": fim.isoformat()},
            "tm_minutos_por_tipo": {
                t: round(soma[t] / qtd[t], 2) if qtd[t] else None for t in soma
            },
            "atendimentos_por_tipo": qtd,
        }

    def auditoria(self, ini: date, fim: date) -> list[dict]:
        linhas = db.session.execute(
            select(AtendimentoAuditoria, Senha, Guiche, Usuario)
            .join(Senha, Senha.id == AtendimentoAuditoria.senha_id)
            .outerjoin(Guiche, Guiche.id == AtendimentoAuditoria.guiche_id)
            .outerjoin(Usuario, Usuario.id == AtendimentoAuditoria.usuario_id)
            .where(Senha.data_emissao >= ini, Senha.data_emissao <= fim)
            .order_by(AtendimentoAuditoria.horario_primeira_chamada)
        ).all()
        return [
            {
                "atendente": u.nome if u else None,
                "guiche": g.numero_guiche if g else None,
                "senha": s.numero_senha,
                "primeira_chamada": a.horario_primeira_chamada,
                "segunda_chamada": a.horario_segunda_chamada,
                "inicio_atendimento": a.horario_inicio_atendimento,
                "fim_atendimento": a.horario_finalizacao_atendimento,
            }
            for a, s, g, u in linhas
        ]

    def indicadores(self, ini: date, fim: date) -> dict:
        senhas = self._senhas(ini, fim)
        total = len(senhas)
        nao_comp = sum(1 for s in senhas if s.status_atual == StatusSenha.NAO_COMPARECEU)
        descartadas = sum(1 for s in senhas if s.descartada_em is not None)

        linhas = db.session.execute(
            select(Senha, AtendimentoAuditoria, Guiche, Usuario)
            .join(AtendimentoAuditoria, AtendimentoAuditoria.senha_id == Senha.id)
            .outerjoin(Guiche, Guiche.id == AtendimentoAuditoria.guiche_id)
            .outerjoin(Usuario, Usuario.id == AtendimentoAuditoria.usuario_id)
            .where(Senha.data_emissao >= ini, Senha.data_emissao <= fim)
        ).all()

        esperas, por_guiche, por_atendente = [], {}, {}
        for senha, aud, guiche, usuario in linhas:
            if aud.horario_primeira_chamada:
                esperas.append(
                    (aud.horario_primeira_chamada - senha.data_hora_emissao).total_seconds() / 60
                )
            if senha.status_atual == StatusSenha.ATENDIDA:
                if guiche:
                    por_guiche[guiche.numero_guiche] = por_guiche.get(guiche.numero_guiche, 0) + 1
                if usuario:
                    por_atendente[usuario.nome] = por_atendente.get(usuario.nome, 0) + 1

        return {
            "periodo": {"inicio": ini.isoformat(), "fim": fim.isoformat()},
            "tempo_medio_espera_min": round(sum(esperas) / len(esperas), 2) if esperas else None,
            "taxa_nao_comparecimento_pct": round(100 * nao_comp / total, 2) if total else 0.0,
            "taxa_descarte_pct": round(100 * descartadas / total, 2) if total else 0.0,
            "atendimentos_por_guiche": por_guiche,
            "atendimentos_por_atendente": por_atendente,
        }