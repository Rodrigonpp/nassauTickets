import React, { useState } from "react";
import "./ModalTotem.css";
import servicos from "../apps/totem/servicos";
import { useEmitirSenha } from "../hooks/useEmitirSenha";

const ModalTotem = ({ modalState, setModalState }) => {
  const servicoAtual = servicos.find((servico) => servico.id === modalState);
  // 1 - Confirmar retirada de senha | 2 - Visualizando a senha
  const [etapa, setEtapa] = useState(1);

  const { senha, dadosOk, loading, erro, emitirSenha, limparSenha } =
    useEmitirSenha();

  const fecharModal = () => {
    setModalState(null);
    setEtapa(1);
    limparSenha();
  };

  const handleGerarSenha = async () => {
    const tipoSenha = servicoAtual.type;
    const resposta = await emitirSenha(tipoSenha);

    if (resposta) {
      setEtapa(2);
    }
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

              {erro && (
                <p className="erro-mensagem" role="alert">
                  {erro}
                </p>
              )}
              <div className="buttons">
                <button
                  className="return"
                  disabled={loading}
                  onClick={() => {
                    fecharModal();
                  }}
                >
                  Voltar
                </button>
                <button
                  className={`confirm botao-${servicoAtual.id}`}
                  disabled={loading}
                  onClick={handleGerarSenha}
                >
                  {loading ? "Gerando..." : "Retirar senha"}
                </button>
              </div>
            </>
          )}
          {etapa === 2 && (
            <>
              <span>SENHA EMITIDA</span>
              <h3>Sua senha é:</h3>
              <p className={`senha senha-${servicoAtual.id}`}>
                {dadosOk && senha ? senha.numero_senha : "----"}
              </p>
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
