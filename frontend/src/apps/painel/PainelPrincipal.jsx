import React from "react";
import Header from "../../components/Header";
import TipoDeSenha from "../../components/TipoDeSenha";
import chamada_icon from "../../assets/chamada.svg";
import chamadas from "./chamadas_mock";
import "./PainelPrincipal.css";

const PainelPrincipal = () => {
  return (
    <>
      <Header />
      <div id="painel-principal">
        <section className="section-chamada-atual">
          <div className="situacao">
            <img src={chamada_icon} alt="chamada em andamento" />
            <h3>CHAMADA EM ANDAMENTO</h3>
          </div>
          <div className="chamada-atual">
            {/* Personalizar com o backend */}
            <TipoDeSenha tipo={"prioritario"} detalhada />
            <h2 className="senha-chamada">260930-SP042</h2>
            <p className="instrucoes">Dirija-se ao</p>
            <p className="guiche">Guichê 03</p>
          </div>
          <p className="documentos">Tenha seu documento em mãos</p>
        </section>
        <section className="ultimas-chamadas">
          <h4>Últimas chamadas</h4>
          <span className="ultimas-span">As 5 senhas mais recentes</span>
          <div className="lista-ultimas-chamadas">
            {chamadas.map((chamada) => (
              <div className="chamada" key={chamada.id}>
                <TipoDeSenha tipo={chamada.tipo} />
                <div className="informacoes-chamada">
                  <p>{chamada.senha}</p>
                  <span>{chamada.hora_chamada}</span>
                </div>
                <span className="ultimas-guiche">Guichê {String(chamada.guiche).padStart(2, "0")}</span>
              </div>
            ))}
          </div>
        </section>
      </div>
    </>
  );
};

export default PainelPrincipal;
