import React from "react";
import servicos from "../apps/totem/servicos";
import "./TipoDeSenha.css";

const TipoDeSenha = ({ tipo, detalhada = false }) => {
  const senha = servicos.find((servico) => servico.id === tipo);

  return (
    <span className={`tipo ${senha.id}`}>
      <img src={senha.img} alt={`${senha.title}`} />
      {`${senha.type} ${detalhada ? ` · ${senha.title}` : ""}`}
    </span>
  );
};

export default TipoDeSenha;
