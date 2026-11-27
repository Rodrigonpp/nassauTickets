import { useEffect, useState } from "react";

// Devolve Date.now() atualizado a cada segundo (usado na contagem regressiva)
export function useAgora() {
  const [agora, setAgora] = useState(() => Date.now());

  useEffect(() => {
    const id = setInterval(() => setAgora(Date.now()), 1000);
    return () => clearInterval(id);
  }, []);

  return agora;
}