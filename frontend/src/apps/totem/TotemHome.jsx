import React, { useState } from "react";
import Header from "../../components/Header";
import Footer from "../../components/Footer";
import ModalTotem from "../../components/ModalTotem";
import servicos from "./servicos";

// Assets
import info from "../../assets/info.svg";

import "./TotemHome.css";

const TotemHome = () => {
  const [modalState, setModalState] = useState(null);

  const retirarSenha = (tipoSenha) => {
    const tiposValidos = ["prioritario", "geral", "exames"];
    if (!tiposValidos.includes(tipoSenha)) return;

    setModalState(tipoSenha);
  };

  return (
    <>
      <Header />
      <div className="totemHome">
        <section className="greetings">
          <h2>Olá! Como podemos ajudar?</h2>
          <p>Toque em uma opção para retirar sua senha.</p>
        </section>
        <section className="retirada-de-senha">
          {servicos.map((servico) => (
            <div
              key={servico.id}
              className={`card ${servico.id}`}
              onClick={(e) => retirarSenha(`${servico.id}`)}
            >
              <img
                src={servico.img}
                alt={`${servico.title}`}
                className={`icon-atendimento icon-${servico.id}`}
              />
              <div
                className={`informacoes-atendimento informacoes-${servico.id}`}
              >
                <span className="tipo">
                  <img src={servico.img} alt={`${servico.title}`} />
                  {servico.type}
                </span>
                <h2 className="tipo-title">{servico.title}</h2>
                <p className="subtitle">{servico.description}</p>
              </div>
              <img src={servico.seta} alt="Avançar" className="seta" />
            </div>
          ))}
        </section>
        <section className="informativo">
          <img src={info} alt="Informativo" />
          <p>
            Senhas prioritárias são chamadas com precedência. Todos os guichês
            atendem todos os tipos.
          </p>
        </section>
      </div>
      <ModalTotem modalState={modalState} setModalState={setModalState} />
      <Footer />
    </>
  );
};

export default TotemHome;
