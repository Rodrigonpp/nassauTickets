import Header from "../../components/Header";
import TipoDeSenha from "../../components/TipoDeSenha";
import chamada_icon from "../../assets/chamada.svg";
import { usePainel } from "../../hooks/usePainel";
import { useNarrador } from "../../hooks/useNarrador";
import "./PainelPrincipal.css";

// Tipo da API (SP/SG/SE) -> id usado pelo componente TipoDeSenha
const TIPO_PARA_ID = { SP: "prioritario", SG: "geral", SE: "exames" };

const STATUS_CHAMANDO = ["CHAMADA", "CHAMADA_NOVAMENTE"];

const ROTULO_SITUACAO = {
  CHAMADA: "CHAMADA EM ANDAMENTO",
  CHAMADA_NOVAMENTE: "CHAMANDO NOVAMENTE",
  EM_ATENDIMENTO: "EM ATENDIMENTO",
  ATENDIDA: "ATENDIMENTO ENCERRADO",
  NAO_COMPARECEU: "SENHA EXPIRADA",
};

// "2026-11-25T09:42:10" -> "09:42"
function formatarHora(iso) {
  return iso ? iso.slice(11, 16) : "--:--";
}

function formatarGuiche(guiche) {
  return guiche != null ? `Guichê ${String(guiche).padStart(2, "0")}` : "Guichê --";
}

const PainelPrincipal = () => {
  const { chamadas, carregado, conectado } = usePainel();
  const { suportado, ativo, ativar, desativar } = useNarrador(
    chamadas,
    carregado,
  );

  // Destaque: a chamada mais recente que ainda está chamando; se não houver
  // nenhuma, a última chamada da lista.
  const destaque =
    chamadas.find((c) => STATUS_CHAMANDO.includes(c.status_atual)) ??
    chamadas[0] ??
    null;

  return (
    <>
      <Header />
      <div id="painel-principal">
        <section className="section-chamada-atual">
          <div className="situacao">
            <img src={chamada_icon} alt="chamada em andamento" />
            <h3>
              {destaque
                ? (ROTULO_SITUACAO[destaque.status_atual] ?? "ÚLTIMA CHAMADA")
                : "AGUARDANDO CHAMADAS"}
            </h3>
          </div>
          <div className="chamada-atual">
            {destaque ? (
              <>
                <TipoDeSenha
                  tipo={TIPO_PARA_ID[destaque.tipo_senha] ?? "geral"}
                  detalhada
                />
                <h2 className="senha-chamada">{destaque.numero_senha}</h2>
                <p className="instrucoes">Dirija-se ao</p>
                <p className="guiche">{formatarGuiche(destaque.guiche)}</p>
              </>
            ) : (
              <>
                <h2 className="senha-chamada">--</h2>
                <p className="instrucoes">Aguarde a próxima chamada</p>
              </>
            )}
          </div>
          <div className="rodape-chamada">
            <p className="documentos">Tenha seu documento em mãos</p>
            {!conectado && (
              <p className="painel-sem-conexao">Sem conexão com o servidor</p>
            )}
            {suportado && (
              <button
                type="button"
                className={`botao-narracao${ativo ? " ativa" : ""}`}
                onClick={ativo ? desativar : ativar}
              >
                {ativo ? "Narração ativada" : "Ativar narração por voz"}
              </button>
            )}
          </div>
        </section>
        <section className="ultimas-chamadas">
          <h4>Últimas chamadas</h4>
          <span className="ultimas-span">As 5 senhas mais recentes</span>
          <div className="lista-ultimas-chamadas">
            {chamadas.length === 0 && (
              <div className="chamada">
                <div className="informacoes-chamada">
                  <p>Nenhuma senha chamada ainda.</p>
                </div>
              </div>
            )}
            {chamadas.map((chamada) => (
              <div className="chamada" key={chamada.numero_senha}>
                <TipoDeSenha tipo={TIPO_PARA_ID[chamada.tipo_senha] ?? "geral"} />
                <div className="informacoes-chamada">
                  <p>{chamada.numero_senha}</p>
                  <span>{formatarHora(chamada.chamada_em)}</span>
                </div>
                <span className="ultimas-guiche">
                  {formatarGuiche(chamada.guiche)}
                </span>
              </div>
            ))}
          </div>
        </section>
      </div>
    </>
  );
};

export default PainelPrincipal;