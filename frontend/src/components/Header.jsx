import React from "react";
import greenCheck from "../assets/check_verde.svg";
import "./Header.css";

const Header = () => {
  return (
    <header id="Header">
      <div className="logo">
        <h1>N</h1>
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
        <p>Escolha do atendimento</p>
      </div>
    </header>
  );
};

export default Header;
