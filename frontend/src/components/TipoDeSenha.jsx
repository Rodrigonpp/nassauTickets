import React from "react";
import servicos from "../apps/totem/servicos";
import "./TipoDeSenha.css";

const TipoDeSenha = ({ tipo }) => {
  const senha = servicos.find((servico) => servico.id === tipo);
  console.log(senha);

  return (
    <span className={`tipo ${senha.id}`}>
      <img src={senha.img} alt={`${senha.title}`} />
      {senha.type}
    </span>
  );
};

export default TipoDeSenha;
