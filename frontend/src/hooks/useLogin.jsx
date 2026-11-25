import { useState, useCallback } from "react";
import { useAuth } from "../contexts/AuthContext";

const URL_LOGIN = "/api/v1/auth/login";

export function useLogin() {
  const { entrar } = useAuth();
  const [loading, setLoading] = useState(false);
  const [erro, setErro] = useState(null);

  // Retorna true se o login deu certo, false caso contrário.
  const autenticar = useCallback(
    async ({ login, senha, manterConectado }) => {
      setLoading(true);
      setErro(null);

      try {
        const response = await fetch(URL_LOGIN, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ login: login.trim(), senha }),
        });

        let data = null;
        try {
          data = await response.json();
        } catch {
          data = null;
        }

        if (!response.ok) {
          if (response.status === 422) {
            throw new Error("Preencha o e-mail e a senha corretamente.");
          }
          throw new Error(
            data && typeof data.mensagem === "string"
              ? data.mensagem
              : `Erro ao fazer login (HTTP ${response.status}).`,
          );
        }

        if (!data || typeof data.access_token !== "string") {
          throw new Error("A resposta da API não veio no formato esperado.");
        }

        entrar(data, manterConectado);
        return true;
      } catch (err) {
        setErro(
          err instanceof TypeError
            ? "Não foi possível conectar ao servidor."
            : err.message,
        );
        return false;
      } finally {
        setLoading(false);
      }
    },
    [entrar],
  );

  return { autenticar, loading, erro };
}
