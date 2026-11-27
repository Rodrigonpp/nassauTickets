import { useEffect, useState } from "react";
import Header from "../../components/Header";
import atendimentoGeral from "../../assets/user.svg";
import atendimentoPrioritario from "../../assets/atendimento_prioritario.svg";
import retiradaExames from "../../assets/retirada_exames.svg";
import TipoDeSenha from "../../components/TipoDeSenha";
import circleCheck from "../../assets/circle-check.svg";
import play from "../../assets/play.svg";
import userX from "../../assets/user-x.svg";
import volume from "../../assets/volume.svg";
import megaphone from "../../assets/megaphone.svg";
import greenCheck from "../../assets/check_verde.svg";
import { useAuth } from "../../contexts/AuthContext";
import { useAtendimento } from "../../hooks/useAtendimento";
import { useAgora } from "../../hooks/useAgora";
import "./DashboardAtendente.css";

const GUICHES = Array.from({ length: 10 }, (_, i) => i + 1);

// Tipo da API (SP/SG/SE) -> id usado pelo componente TipoDeSenha
const TIPO_PARA_ID = { SP: "prioritario", SG: "geral", SE: "exames" };

const ROTULO_STATUS = {
  CHAMADA: "Chamada",
  CHAMADA_NOVAMENTE: "Chamada novamente",
  EM_ATENDIMENTO: "Em atendimento",
  ATENDIDA: "Encerrado",
  NAO_COMPARECEU: "Não compareceu",
};

function lerGuicheSalvo(chave) {
  try {
    const salvo = Number(localStorage.getItem(chave));
    return GUICHES.includes(salvo) ? salvo : GUICHES[0];
  } catch {
    return GUICHES[0];
  }
}

// "2026-11-25T09:42:10" -> "09:42"
function formatarHora(iso) {
  return iso ? iso.slice(11, 16) : "--:--";
}

// Segundos -> "mm:ss"
function formatarContagem(totalSegundos) {
  const m = Math.floor(totalSegundos / 60);
  const s = totalSegundos % 60;
  return `${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}`;
}

const DashboardAtendente = () => {
  const dataHoje = new Date().toLocaleDateString("pt-BR", {
    dateStyle: "long",
  });

  const { usuario, sair } = useAuth();
  const chaveGuiche = `nassau_guiche_${usuario?.id}`;
  const [guicheId, setGuicheId] = useState(() => lerGuicheSalvo(chaveGuiche));

  const {
    fila,
    atual,
    ultimas,
    conectado,
    carregando,
    processando,
    erro,
    limparErro,
    chamarProxima,
    iniciar,
    chamarNovamente,
    naoCompareceu,
    encerrar,
    atualizar,
  } = useAtendimento();

  const alterarGuiche = (e) => {
    const novo = Number(e.target.value);
    setGuicheId(novo);
    try {
      localStorage.setItem(chaveGuiche, String(novo));
    } catch {
      // armazenamento indisponível: segue só em memória
    }
  };

  const totalPrioritario = fila.SP;
  const totalExames = fila.SE;
  const totalGeral = fila.SG;

  const totalSenhas = totalPrioritario + totalGeral + totalExames;

  // Regras da máquina de estados do backend
  const status = atual?.status_atual;
  const bloqueado = carregando || processando;
  const podeIniciar = status === "CHAMADA" || status === "CHAMADA_NOVAMENTE";
  const podeChamarNovamente = status === "CHAMADA";
  const podeNaoCompareceu = status === "CHAMADA_NOVAMENTE";
  const podeEncerrar = status === "EM_ATENDIMENTO";
  const podeChamarProxima = !atual && totalSenhas > 0;

  // Prazo de comparecimento (regra no backend): 1 min na 1ª chamada, depois a
  // senha é chamada novamente e, após mais 1 min, expira (não compareceu).
  const agora = useAgora();
  const segundosRestantes =
    atual?.fim_prazo != null
      ? Math.min(
          atual.prazo_segundos,
          Math.max(0, Math.ceil((atual.fim_prazo - agora) / 1000)),
        )
      : null;
  const prazoEsgotado = segundosRestantes === 0;

  const dicaTempo =
    status === "CHAMADA"
      ? "até chamar novamente"
      : status === "CHAMADA_NOVAMENTE"
        ? "até a senha expirar"
        : "";

  // Zerou o relógio: pede o estado ao backend, que aplica a rechamada/expiração.
  useEffect(() => {
    if (!prazoEsgotado) return undefined;
    const primeira = setTimeout(atualizar, 500);
    const repetir = setInterval(atualizar, 2000);
    return () => {
      clearTimeout(primeira);
      clearInterval(repetir);
    };
  }, [prazoEsgotado, atualizar]);

  const textoProximaSenha = atual
    ? "Finalize o atendimento atual para chamar a próxima senha."
    : totalSenhas > 0
      ? "Há senhas aguardando. Chame a próxima da fila."
      : "Não há senhas aguardando no momento.";

  const resumoSenhasCard = [
    {
      id: 1,
      titulo: "Total na fila",
      total: totalSenhas,
      texto: "pessoas aguardando",
      img: atendimentoGeral,
    },
    {
      id: 2,
      titulo: "Prioritárias",
      total: totalPrioritario,
      texto: "Atendimento prioritário",
      img: atendimentoPrioritario,
    },
    {
      id: 3,
      titulo: "Exames",
      total: totalExames,
      texto: "Retirada de exames",
      img: retiradaExames,
    },
    {
      id: 4,
      titulo: "Geral",
      total: totalGeral,
      texto: "Atendimento geral",
      img: atendimentoGeral,
    },
  ];

  return (
    <>
      <Header />
      <div id="dashboard">
        <section className="dashboard-presentation">
          <div className="central-atendimento-container">
            <h2 className="central-atendimento">Central de atendimento</h2>
            <span className="central-atendimento-subtitle">
              Gerencie as chamadas e o atendimento sem sair desta tela.
            </span>
          </div>
          <div className="informacoes-atendente">
            <p className="data-hoje">{dataHoje}</p>
            <p className="unidade-guiche">
              Unidade Nassau -
              <select
                className="seletor-guiche"
                aria-label="Guichê"
                value={guicheId}
                onChange={alterarGuiche}
                disabled={Boolean(atual)}
              >
                {GUICHES.map((n) => (
                  <option key={n} value={n}>
                    Guichê {String(n).padStart(2, "0")}
                  </option>
                ))}
              </select>
            </p>
            <p className="usuario-logado">
              {usuario?.nome}
              <button type="button" className="sair-atendente" onClick={sair}>
                Sair
              </button>
            </p>
          </div>
        </section>
        {erro && (
          <div className="erro-dashboard" role="alert">
            <span>{erro}</span>
            <button
              type="button"
              onClick={limparErro}
              aria-label="Fechar aviso"
            >
              ×
            </button>
          </div>
        )}
        <section className="resumo-senhas">
          {resumoSenhasCard.map((card) => (
            <div className="card-resumo-senhas" key={card.id}>
              <div className="categoria">
                <p className="titulo-card">{card.titulo}</p>
                <img src={card.img} alt={card.texto} />
              </div>
              <div className="quantidade-fila">
                <p>
                  {card.total} <span className="texto-fila">{card.texto}</span>
                </p>
              </div>
            </div>
          ))}
        </section>
        <section className="atendimento-ultimas-chamadas">
          <div className="senha-atual-opcoes">
            <div className="estado-senha">
              <p className="senha-atual-title">Senha atual</p>
            </div>
            <div className="senha-e-tempo-duracao">
              <div className="identificacao-senha">
                {atual ? (
                  <>
                    <TipoDeSenha
                      tipo={TIPO_PARA_ID[atual.tipo_senha] ?? "geral"}
                      detalhada
                    />
                    <h3 className="senha-atual">{atual.numero_senha}</h3>
                  </>
                ) : (
                  <>
                    <h3 className="senha-atual">--</h3>
                    <span className="sem-senha-atual">
                      Nenhuma senha em atendimento
                    </span>
                  </>
                )}
              </div>
              <div className="tempo-de-espera">
                <span>Tempo de espera</span>
                <p
                  className={`wait-time${
                    segundosRestantes !== null && segundosRestantes <= 10
                      ? " urgente"
                      : ""
                  }`}
                >
                  {segundosRestantes !== null
                    ? formatarContagem(segundosRestantes)
                    : "--:--"}
                </p>
                {dicaTempo && <small className="dica-tempo">{dicaTempo}</small>}
              </div>
            </div>
            <div className="acoes-senha">
              <button
                className="iniciar-atendimento"
                onClick={iniciar}
                disabled={bloqueado || !podeIniciar}
              >
                <img src={play} />
                Iniciar atendimento
              </button>
              <button
                className="chamar-novamente"
                onClick={chamarNovamente}
                disabled={bloqueado || !podeChamarNovamente}
              >
                <img src={volume} />
                Chamar novamente
              </button>
              <button
                className="nao-compareceu"
                onClick={naoCompareceu}
                disabled={bloqueado || !podeNaoCompareceu}
              >
                <img src={userX} />
                Não compareceu
              </button>
              <button
                className="encerrar-atendimento"
                onClick={encerrar}
                disabled={bloqueado || !podeEncerrar}
              >
                <img src={circleCheck} />
                Encerrar atendimento
              </button>
            </div>
            <div className="proxima-chamada">
              <div className="orientacoes-proxima-senha">
                <p>Próxima senha</p>
                <span>{textoProximaSenha}</span>
              </div>
              <button
                className="chamar-proxima-senha"
                onClick={() => chamarProxima(guicheId)}
                disabled={bloqueado || !podeChamarProxima}
              >
                <img src={megaphone} />
                Chamar próxima senha
              </button>
            </div>
          </div>
          <div className="ultimas-senhas-chamadas">
            <strong>Últimas senhas chamadas</strong>
            <ul className="lista-ultimas-senhas">
              {ultimas.length === 0 && (
                <li className="senha-chamada-lista">
                  <strong>Nenhuma senha chamada ainda.</strong>
                </li>
              )}
              {ultimas.map((item) => (
                <li className="senha-chamada-lista" key={item.id}>
                  <TipoDeSenha
                    tipo={TIPO_PARA_ID[item.tipo_senha] ?? "geral"}
                  />
                  <strong>{item.numero_senha}</strong>
                  <div className="horario-e-situacao">
                    <span className="hora-chamada">
                      {formatarHora(item.ultima_chamada_em)}
                    </span>
                    <span className="situacao-senha-listada">
                      {ROTULO_STATUS[item.status_atual] ?? item.status_atual}
                    </span>
                  </div>
                </li>
              ))}
            </ul>
          </div>
        </section>
        <section className="status-painel">
          <span className={`conexao-painel${conectado ? "" : " sem-conexao"}`}>
            {conectado ? (
              <>
                <img src={greenCheck} /> Painel conectado
              </>
            ) : (
              "Sem conexão com o servidor"
            )}
          </span>
          <span className="prioridade-alternancia">
            Prioridade e alternância aplicadas automaticamente · SP → SE | SG
          </span>
        </section>
      </div>
    </>
  );
};

export default DashboardAtendente;
