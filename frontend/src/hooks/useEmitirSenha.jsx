import { useState, useCallback } from "react";

const TIPOS_VALIDOS = ["SP", "SG", "SE"];
const URL_SENHAS = "/api/v1/senhas";

function validarRespostaSenha(payload) {
  return Boolean(
    payload &&
    typeof payload === "object" &&
    typeof payload.numero_senha === "string" &&
    payload.numero_senha.trim() !== "" &&
    typeof payload.tipo_senha === "string" &&
    typeof payload.status_atual === "string" &&
    typeof payload.data_hora_emissao === "string",
  );
}

export function useEmitirSenha() {
  const [senha, setSenha] = useState(null);
  const [loading, setLoading] = useState(false);
  const [erro, setErro] = useState(null);
  const [dadosOk, setDadosOk] = useState(false);

  const emitirSenha = useCallback(async (tipo) => {
    const tipoNormalizado =
      typeof tipo === "string" ? tipo.trim().toUpperCase() : "";

    if (!TIPOS_VALIDOS.includes(tipoNormalizado)) {
      const mensagem = `Tipo de senha inválido (${tipo}). Use "SP", "SG" ou "SE".`;
      setErro(mensagem);
      setDadosOk(false);
      return null;
    }

    setLoading(true);
    setErro(null);
    setDadosOk(false);

    try {
      const response = await fetch(URL_SENHAS, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ tipo: tipoNormalizado }),
      });

      let data = null;
      try {
        data = await response.json();
      } catch {
        data = null;
      }

      if (!response.ok) {
        const mensagemBackend =
          data && typeof data.message === "string"
            ? data.message
            : `Erro ao emitir senha (HTTP ${response.status})`;
        throw new Error(mensagemBackend);
      }

      if (!validarRespostaSenha(data)) {
        throw new Error("A resposta da API não veio no formato esperado.");
      }

      setSenha(data);
      setDadosOk(true);
      return data;
    } catch (err) {
      setSenha(null);
      setDadosOk(false);
      setErro(
        err instanceof Error ? err.message : "Erro inesperado ao emitir senha.",
      );
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  const limparSenha = useCallback(() => {
    setSenha(null);
    setErro(null);
    setDadosOk(false);
  }, []);

  return {
    senha,
    dadosOk,
    loading,
    erro,
    emitirSenha,
    limparSenha,
  };
}
