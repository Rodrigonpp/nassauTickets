import React, { useState } from "react";
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

const DashboardAtendente = () => {
  const dataHoje = new Date().toLocaleDateString("pt-BR", {
    dateStyle: "long",
  });

  const [totalPrioritario, setTotalPrioritario] = useState(0);
  const [totalExames, setTotalExames] = useState(0);
  const [totalGeral, setTotalGeral] = useState(0);

  const totalSenhas = totalPrioritario + totalGeral + totalExames;

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

  const listaSenhas = [
    {
      id: 1,
      sigla: "SP",
      senha: "260930-SP042",
      tipo: "prioritario",
      horario: "09:42",
      status: "Aguardando",
    },
    {
      id: 2,
      sigla: "SE",
      senha: "260930-SE018",
      tipo: "exames",
      horario: "09:30",
      status: "Encerrado",
    },
    {
      id: 3,
      sigla: "SG",
      senha: "260930-SG037",
      tipo: "geral",
      horario: "09:23",
      status: "Encerrado",
    },
    {
      id: 4,
      sigla: "SP",
      senha: "260930-SP041",
      tipo: "prioritario",
      horario: "09:21",
      status: "Não compareceu",
    },
    {
      id: 5,
      sigla: "SG",
      senha: "260930-SG036",
      tipo: "geral",
      horario: "09:12",
      status: "Encerrado",
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
              <span className="guiche-atendente"> Guichê 01</span>
            </p>
          </div>
        </section>
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
                <TipoDeSenha tipo={"prioritario"} detalhada />
                <h3 className="senha-atual">260930-SP042</h3>
              </div>
              <div className="tempo-de-espera">
                <span>Tempo de espera</span>
                <span className="wait-time">00:26</span>
              </div>
              <div className="acoes-senha">
                <button className="iniciar-atendimento">
                  <img src={play} />
                  Iniciar atendimento
                </button>
                <button className="chamar-novamente">
                  <img src={volume} />
                  Chamar novamente
                </button>
                <button className="nao-compareceu">
                  <img src={userX} />
                  Não compareceu
                </button>
                <button className="Encerrar atendimento">
                  <img src={circleCheck} />
                  Encerrar atendimento
                </button>
              </div>
            </div>
            <div className="proxima-chamada">
              <div className="orientacoes-proxima-senha">
                <p>Próxima senha</p>
                <span>
                  Finalize o atendimento atual para chamar a próxima senha.
                </span>
              </div>
              <button className="chamar-proxima-senha">
                <img src={megaphone} />
                Chamar próxima senha
              </button>
            </div>
          </div>
          <div className="ultimas-senhas-chamadas">
            <strong>Últimas senhas chamadas</strong>
            <ul className="lista-ultimas-senhas">
              {listaSenhas.map((item) => (
                <li className="senha-chamada-lista" key={item.id}>
                  <TipoDeSenha tipo={item.tipo} />
                  <strong>{item.senha}</strong>
                  <div className="horario-e-situacao">
                    <span className="hora-chamada">{item.horario}</span>
                    <span className="situacao-senha-listada">
                      {item.status}
                    </span>
                  </div>
                </li>
              ))}
            </ul>
          </div>
        </section>
        <section className="status-painel"></section>
      </div>
    </>
  );
};

export default DashboardAtendente;
