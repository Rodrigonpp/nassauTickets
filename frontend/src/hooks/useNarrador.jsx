import { useCallback, useEffect, useRef, useState } from "react";

const suportado = typeof window !== "undefined" && "speechSynthesis" in window;

function falar(texto) {
  if (!suportado) return;
  const fala = new SpeechSynthesisUtterance(texto);
  fala.lang = "pt-BR";
  fala.rate = 0.9;
  const vozes = window.speechSynthesis.getVoices();
  const voz =
    vozes.find((v) => v.lang === "pt-BR") ||
    vozes.find((v) => v.lang && v.lang.toLowerCase().startsWith("pt"));
  if (voz) fala.voice = voz;
  window.speechSynthesis.speak(fala);
}

// "SP", 42, 3 -> "Senha S P 42, dirija-se ao guichê 3."
function textoDaChamada(chamada) {
  const letras = chamada.tipo_senha.split("").join(" ");
  const guiche =
    chamada.guiche != null ? `, dirija-se ao guichê ${chamada.guiche}` : "";
  return `Senha ${letras} ${chamada.sequencial}${guiche}.`;
}

// Lê em voz alta cada senha NOVA que aparece em `chamadas`, uma única vez.
// - a 1ª resposta do painel só serve de referência (não narra o que já estava lá)
// - rechamar uma senha já conhecida não narra de novo
// - o navegador só libera áudio após um clique: por isso existe ativar()
export function useNarrador(chamadas, carregado) {
  const [ativo, setAtivo] = useState(false);
  const jaVistas = useRef(null); // Set com os numero_senha já conhecidos

  useEffect(() => {
    if (!carregado) return;

    if (jaVistas.current === null) {
      jaVistas.current = new Set(chamadas.map((c) => c.numero_senha));
      return;
    }

    const novas = chamadas.filter((c) => !jaVistas.current.has(c.numero_senha));
    if (novas.length === 0) return;

    novas.forEach((c) => jaVistas.current.add(c.numero_senha));
    if (ativo) {
      // a lista vem da mais recente para a mais antiga: narra na ordem das chamadas
      [...novas].reverse().forEach((c) => falar(textoDaChamada(c)));
    }
  }, [chamadas, carregado, ativo]);

  const ativar = useCallback(() => {
    if (!suportado) return;
    window.speechSynthesis.cancel();
    falar("Narração ativada.");
    setAtivo(true);
  }, []);

  const desativar = useCallback(() => {
    if (suportado) window.speechSynthesis.cancel();
    setAtivo(false);
  }, []);

  return { suportado, ativo, ativar, desativar };
}