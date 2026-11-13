import React from "react";
import { useNavigate } from "react-router-dom";
import { useNavigation } from "../contexts/NavigationContext";
import greenCheck from "../assets/check_verde.svg";
import "./Header.css";

const Header = () => {
  const navigate = useNavigate();

  const { currentScreen } = useNavigation();

  return (
    <header id="Header">
      <div className="logo">
        <h1
          onClick={() => {
            navigate("/");
          }}
        >
          N
        </h1>
        <div className="presentation">
          <h2>nassauTickets</h2>
          <p>Laboratório de Análises Clínicas</p>
        </div>
      </div>
      <div className="totem-status">
        <span className="green-check">
          <img src={greenCheck} alt="Sistema conectado" />
          Sistema conectado
        </span>
        {/* Pode ser alterado com um contexto para atualizar de acordo */}
        {currentScreen === "home" && <p>Central de acesso</p>}
        {currentScreen === "totem" && <p>Escolha do atendimento</p>}
      </div>
    </header>
  );
};

export default Header;
