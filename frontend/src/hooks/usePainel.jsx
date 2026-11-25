import { useEffect, useState } from "react";

const URL_PAINEL = "http://localhost:5000/api/v1/painel";
const INTERVALO_ATUALIZACAO_MS = 3000;

// GET /api/v1/painel (público): últimas 5 senhas chamadas, a mais recente primeiro
export function usePainel() {
  const [chamadas, setChamadas] = useState([]);
  const [carregado, setCarregado] = useState(false); // já houve 1 resposta?
  const [conectado, setConectado] = useState(true);

  useEffect(() => {
    let ativo = true;

    const buscar = async () => {
      try {
        const response = await fetch(URL_PAINEL);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const data = await response.json();
        if (!ativo) return;
        setChamadas(Array.isArray(data) ? data : []);
        setConectado(true);
        setCarregado(true);
      } catch {
        if (ativo) setConectado(false);
      }
    };

    const primeiraBusca = setTimeout(buscar, 0);
    const id = setInterval(buscar, INTERVALO_ATUALIZACAO_MS);
    return () => {
      ativo = false;
      clearTimeout(primeiraBusca);
      clearInterval(id);
    };
  }, []);

  return { chamadas, carregado, conectado };
}