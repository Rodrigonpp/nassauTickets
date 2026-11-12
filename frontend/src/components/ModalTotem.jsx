import React, { useState } from "react";
import "./ModalTotem.css";
import servicos from "../apps/totem/servicos";

const ModalTotem = ({ modalState, setModalState }) => {
  const servicoAtual = servicos.find((servico) => servico.id === modalState);
  // 1 - Confirmar retirada de senha | 2 - Visualizando a senha
  const [etapa, setEtapa] = useState(1);

  const fecharModal = () => {
    setModalState(null);
    setEtapa(1);
  };

  return (
    modalState && (
      <div
        className="modal-overlay"
        onClick={() => {
          fecharModal();
        }}
      >
        <div className="modal-container" onClick={(e) => e.stopPropagation()}>
          {etapa === 1 && (
            <>
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
                    fecharModal();
                  }}
                >
                  Voltar
                </button>
                <button
                  className={`confirm botao-${servicoAtual.id}`}
                  onClick={() => setEtapa(2)}
                >
                  Retirar senha
                </button>
              </div>
            </>
          )}
          {etapa === 2 && (
            <>
              <span>SENHA EMITIDA</span>
              <h3>Sua senha é:</h3>
              <p className={`senha senha-${servicoAtual.id}`}>XXXX</p>
              <span className="orientacao">Aguarde a chamada no painel</span>
              <button
                className={`concluir botao-${servicoAtual.id}`}
                onClick={() => fecharModal()}
              >
                Concluir
              </button>
            </>
          )}
        </div>
      </div>
    )
  );
};

export default ModalTotem;
