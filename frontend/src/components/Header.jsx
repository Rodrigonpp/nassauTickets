import React from "react";
import { useNavigate } from "react-router-dom";
import { useNavigation } from "../contexts/NavigationContext";
import greenCheck from "../assets/check_verde.svg";
import "./Header.css";
import { useTheme } from "../contexts/ThemeContext";

const Header = () => {
  const navigate = useNavigate();

  const { currentScreen } = useNavigation();
  const { theme } = useTheme();
  console.log(theme);

  return (
    <header id="Header" className={theme}>
      <div className="logo">
        <h1
          className={theme}
          onClick={() => {
            navigate("/");
          }}
        >
          N
        </h1>
        <div className="presentation">
          <h2 className={theme}>nassauTickets</h2>
          <p className={theme}>Laboratório de Análises Clínicas</p>
        </div>
      </div>
      <div className="totem-status">
        <span className={`green-check ${theme}`}>
          <img src={greenCheck} alt="Sistema conectado" />
          Sistema conectado
        </span>
        {/* Pode ser alterado com um contexto para atualizar de acordo */}
        {currentScreen === "home" && <p>Central de acesso</p>}
        {currentScreen === "totem" && <p>Escolha do atendimento</p>}
        {currentScreen === "painel" && (
          <p className={theme}>Painel de chamadas</p>
        )}
        {currentScreen === "atendente" && <p>Atendente</p>}
      </div>
    </header>
  );
};

export default Header;
