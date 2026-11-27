import React from "react";
import "./Footer.css";
import acessibilidade from "../assets/acessibilidade.svg";

const Footer = () => {
  return (
    <footer id="Footer">
      <div className="atendimento">
        <p>Atendimento hoje: 07h-17h</p>
      </div>
      <div className="acessibilidade">
        <span className="accessibility">
          <img src={acessibilidade} alt="Acessibilidade" />
          Ajuda de acessibilidade
        </span>
      </div>
    </footer>
  );
};

export default Footer;
