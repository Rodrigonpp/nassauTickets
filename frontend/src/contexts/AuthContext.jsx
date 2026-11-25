import {
  createContext,
  useCallback,
  useContext,
  useMemo,
  useState,
} from "react";

const AuthContext = createContext();
const CHAVE_SESSAO = "nassau_auth";

function lerSessao() {
  try {
    const bruto =
      localStorage.getItem(CHAVE_SESSAO) ??
      sessionStorage.getItem(CHAVE_SESSAO);
    return bruto ? JSON.parse(bruto) : null;
  } catch {
    return null;
  }
}

export function AuthProvider({ children }) {
  const [sessao, setSessao] = useState(lerSessao);

  const entrar = useCallback((dados, manterConectado) => {
    localStorage.removeItem(CHAVE_SESSAO);
    sessionStorage.removeItem(CHAVE_SESSAO);

    const armazenamento = manterConectado ? localStorage : sessionStorage;
    armazenamento.setItem(CHAVE_SESSAO, JSON.stringify(dados));
    setSessao(dados);
  }, []);

  const sair = useCallback(() => {
    localStorage.removeItem(CHAVE_SESSAO);
    sessionStorage.removeItem(CHAVE_SESSAO);
    setSessao(null);
  }, []);

  const value = useMemo(
    () => ({
      token: sessao?.access_token ?? null,
      usuario: sessao
        ? { id: sessao.usuario_id, nome: sessao.nome, perfil: sessao.perfil }
        : null,
      autenticado: Boolean(sessao?.access_token),
      entrar,
      sair,
    }),
    [sessao, entrar, sair],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error("useAuth deve ser usado dentro de um AuthProvider");
  }

  return context;
}