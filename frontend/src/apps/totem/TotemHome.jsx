import React from "react";
import Header from "../../components/Header";
import Footer from "../../components/Footer";

// Assets
import info from "../../assets/info.svg";
import atendimento_prioritario from "../../assets/atendimento_prioritario.svg";
import user from "../../assets/user.svg";
import retirada_exames from "../../assets/retirada_exames.svg";
import seta_azul from "../../assets/seta_azul.svg"
import seta_laranja from "../../assets/seta_laranja.svg"
import seta_roxa from "../../assets/seta_roxa.svg"

import "./TotemHome.css";

const TotemHome = () => {
  return (
    <>
      <Header />
      <div className="totemHome">
        <section className="greetings">
          <h2>Olá! Como podemos ajudar?</h2>
          <p>Toque em uma opção para retirar sua senha.</p>
        </section>
        <section className="retirada-de-senha">
          <div className="prioritario cor-prioritario">
            <img
              src={atendimento_prioritario}
              alt="Atendimento prioritário "
              className="icon-atendimento cor-prioritario"
            />
            <div className="informacoes-atendimento">
              <span className="tipo">
                <img
                  src={atendimento_prioritario}
                  alt="Atendimento prioritário"
                  className="cor-prioritario"
                />
                SP
              </span>
              <h2 className="tipo-title">Atendimento prioritário</h2>
              <p className="subtitle">Pessoas com prioridade prevista em lei</p>
            </div>
            <img src={seta_laranja} alt="" className="seta" />
          </div>
          {/* parei aqui fazer o resto dos botões de fila */}
          <div className="geral">Atendimento geral</div>
          <div className="exames">Retirada de exames</div>
        </section>
        <section className="informativo">
          <span>
            <img src={info} alt="Informativo" />
            Senhas prioritárias são chamadas com precedência. Todos os guichês
            atendem todos os tipos.
          </span>
        </section>
      </div>
      <Footer />
    </>
  );
};

export default TotemHome;
