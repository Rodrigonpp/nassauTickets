import React from "react";
import Header from "../../components/Header";
import TipoDeSenha from "../../components/TipoDeSenha";

const PainelPrincipal = () => {
  return (
    <>
      <Header />
      <div id="painel-principal">
        <section className="chamada-atual">
          <TipoDeSenha tipo={"prioritario"} />
          <TipoDeSenha tipo={"geral"} />
          <TipoDeSenha tipo={"exames"} />
        </section>
        <section className="ultimas-chamadas"></section>
      </div>
    </>
  );
};

export default PainelPrincipal;
