import React from "react";
import "./ModalTotem.css";
import servicos from "../apps/totem/servicos";

const ModalTotem = ({ modalState, setModalState }) => {
  const servicoAtual = servicos.find((servico) => servico.id === modalState);

  return (
    modalState && (
      <div
        className="modal-overlay"
        onClick={() => {
          setModalState(null);
        }}
      >
        <div className="modal-container" onClick={(e) => e.stopPropagation()}>
          <img
            src={servicoAtual.img}
            alt={servicoAtual.title}
            className={`modal-icon modal-icon-${servicoAtual.id}`}
          />
          <span>Confirmar atendimento</span>
          <h3>{servicoAtual.title}</h3>
          <p>{servicoAtual.description}</p>
          <div className="buttons">
            <button
              className="return"
              onClick={() => {
                setModalState(null);
              }}
            >
              Voltar
            </button>
            <button className={`confirm botao-${servicoAtual.id}`}>
              Retirar senha
            </button>
          </div>
        </div>
      </div>
    )
  );
};

export default ModalTotem;
