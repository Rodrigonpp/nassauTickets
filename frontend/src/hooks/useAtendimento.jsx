import { useCallback, useEffect, useState } from "react";
import { useAuth } from "../contexts/AuthContext";

const URL_BASE = "/api/v1/atendimentos";
const INTERVALO_ATUALIZACAO_MS = 5000;
const FILA_VAZIA = { SP: 0, SG: 0, SE: 0 };

function extrairMensagem(status, data) {
  // Erros de regra de negócio: { codigo, mensagem }
  if (data && typeof data.mensagem === "string") return data.mensagem;
  // Erro de validação do flask-smorest: { code, errors, status }
  if (status === 422 && data && data.errors) return "Dados inválidos.";
  return `Erro na requisição (HTTP ${status}).`;
}

async function requisitar(url, token, { metodo = "GET", corpo } = {}) {
  const response = await fetch(url, {
    method: metodo,
    headers: {
      Authorization: `Bearer ${token}`,
      ...(corpo ? { "Content-Type": "application/json" } : {}),
    },
    body: corpo ? JSON.stringify(corpo) : undefined,
  });

  const data = await response.json().catch(() => null);

  if (!response.ok) {
    const erro = new Error(extrairMensagem(response.status, data));
    // Token ausente/expirado (401) ou inválido (422 com { msg })
    erro.sessaoExpirada =
      response.status === 401 ||
      (response.status === 422 && typeof data?.msg === "string");
    throw erro;
  }

  return data;
}

export function useAtendimento() {
  const { token, sair } = useAuth();

  const [estado, setEstado] = useState({
    fila: FILA_VAZIA,
    atual: null,
    ultimas: [],
  });
  const [carregando, setCarregando] = useState(true);
  const [conectado, setConectado] = useState(true);
  const [processando, setProcessando] = useState(false);
  const [erro, setErro] = useState(null);

  // GET /api/v1/atendimentos/estado
  const atualizar = useCallback(async () => {
    try {
      const data = await requisitar(`${URL_BASE}/estado`, token);
      setEstado({
        fila: { ...FILA_VAZIA, ...data.fila },
        atual: data.atual
          ? {
              ...data.atual,
              // instante (no relógio deste navegador) em que o prazo vence
              fim_prazo:
                data.atual.segundos_restantes != null
                  ? Date.now() + data.atual.segundos_restantes * 1000
                  : null,
            }
          : null,
        ultimas: data.ultimas ?? [],
      });
      setConectado(true);
    } catch (err) {
      if (err.sessaoExpirada) {
        sair();
      } else if (err instanceof TypeError) {
        setConectado(false); // servidor fora do ar / sem rede
      } else {
        setErro(err.message);
      }
    } finally {
      setCarregando(false);
    }
  }, [token, sair]);

  // Busca ao abrir a tela e repete a cada INTERVALO_ATUALIZACAO_MS
  useEffect(() => {
    const primeiraBusca = setTimeout(atualizar, 0);
    const id = setInterval(atualizar, INTERVALO_ATUALIZACAO_MS);
    return () => {
      clearTimeout(primeiraBusca);
      clearInterval(id);
    };
  }, [atualizar]);

  // Executa uma ação (POST) e recarrega o estado. Retorna true/false.
  const executar = useCallback(
    async (caminho, corpo) => {
      setProcessando(true);
      setErro(null);

      try {
        await requisitar(`${URL_BASE}${caminho}`, token, {
          metodo: "POST",
          corpo,
        });
        await atualizar();
        return true;
      } catch (err) {
        if (err.sessaoExpirada) {
          sair();
          return false;
        }
        setErro(
          err instanceof TypeError
            ? "Não foi possível conectar ao servidor."
            : err.message,
        );
        await atualizar(); // re-sincroniza (ex.: o estado mudou em outra aba)
        return false;
      } finally {
        setProcessando(false);
      }
    },
    [token, sair, atualizar],
  );

  const acaoSobreAtual = useCallback(
    (acao) => {
      if (!estado.atual) return Promise.resolve(false);
      return executar(`/${estado.atual.id}/${acao}`);
    },
    [estado.atual, executar],
  );

  // POST /api/v1/atendimentos/chamar-proximo
  const chamarProxima = useCallback(
    (guicheId) => executar("/chamar-proximo", { guiche_id: guicheId }),
    [executar],
  );

  return {
    fila: estado.fila,
    atual: estado.atual,
    ultimas: estado.ultimas,
    atualizar,
    carregando,
    conectado,
    processando,
    erro,
    limparErro: () => setErro(null),
    chamarProxima,
    // POST /api/v1/atendimentos/{senha_id}/iniciar
    iniciar: () => acaoSobreAtual("iniciar"),
    // POST /api/v1/atendimentos/{senha_id}/chamar-novamente
    chamarNovamente: () => acaoSobreAtual("chamar-novamente"),
    // POST /api/v1/atendimentos/{senha_id}/nao-compareceu
    naoCompareceu: () => acaoSobreAtual("nao-compareceu"),
    // POST /api/v1/atendimentos/{senha_id}/encerrar
    encerrar: () => acaoSobreAtual("encerrar"),
  };
}
