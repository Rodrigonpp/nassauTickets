import React from "react";
import Header from "../components/Header";
import totem_icon from "../assets/totem-icon.svg";
import painel_icon from "../assets/painel-icon.svg";
import atendente_icon from "../assets/atendente-icon.svg";
import lock_icon from "../assets/lock-icon.svg";
import seta_simples from "../assets/seta_simples.svg";

import "./Home.css";
import Footer from "../components/Footer";
import { useNavigate } from "react-router-dom";

const Home = () => {
  const navigate = useNavigate();

  const perfis = [
    {
      id: "totem",
      subtitle: "autoatendimento",
      description:
        "Retire uma senha e escolha o tipo de atendimento de forma simples e rápida.",
      img: totem_icon,
      link: "/totem",
    },
    {
      id: "painel",
      subtitle: "chamadas em tempo real",
      description:
        "Acompanhe as senhas chamadas e a indicação dos guichês de atendimento.",
      img: painel_icon,
      link: "/painel",
    },
    {
      id: "atendente",
      subtitle: "gestão do atendimento",
      description:
        "Acesse sua estação para organizar a fila, chamar senhas e realizar atendimentos.",
      img: atendente_icon,
      link: "/atendente/login",
    },
  ];

  return (
    <>
      <Header />
      <div id="Home">
        <section className="presentation-home">
          <span className="greetings-home">BEM-VINDO AO NASSAUTICKETS</span>
          <h1 className="main-title">Como você deseja acessar?</h1>
          <p className="subtitle">
            Selecione o perfil que melhor se adequa às suas necessidades.
          </p>
        </section>
        <section className="perfis">
          {perfis.map((perfil) => (
            <div className="perfil" key={perfil.id}>
              <div className="header-perfil">
                <img src={perfil.img} alt={perfil.id} className="img-perfil" />
                <p className="subtitulo">{perfil.subtitle}</p>
              </div>
              <div className="descricao-perfil">
                <h3 className="perfil-titulo">{perfil.id}</h3>
                <p className="descricao">{perfil.description}</p>
              </div>
              <button
                className="btn-perfil"
                onClick={() => navigate(perfil.link)}
              >
                Acessar {perfil.id} <img src={seta_simples} />
              </button>
            </div>
          ))}
        </section>
        <section className="aviso">
          <span className="aviso-atendente">
            <img
              src={lock_icon}
              alt="O perfil Atendente requer credenciais institucionais."
            />
            O perfil Atendente requer credenciais institucionais.
          </span>
        </section>
      </div>
      <Footer />
    </>
  );
};

export default Home;
