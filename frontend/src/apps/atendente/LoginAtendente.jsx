import React from "react";
import Header from "../../components/Header";
import safety_shield from "../../assets/safety_shield.svg";
import check from "../../assets/check.svg";
import "./LoginAtendente.css";

const LoginAtendente = () => {
  return (
    <>
      <Header />
      <div className="login-atendente">
        <section className="login-presentation">
          <div className="informacoes-login">
            <div className="ambiente-seguro">
              <img src={safety_shield} alt="Ambiente seguro" />
              <p>AMBIENTE SEGURO</p>
            </div>
            <h2>Atendimento claro, humano e eficiente.</h2>
            <span>
              Acesse sua estação para organizar a fila e conduzir cada
              atendimento com segurança.
            </span>
            <ul className="topicos-login">
              <li>
                <img src={check} />
                Qualquer guichê atende qualquer tipo de senha
              </li>
              <li>
                <img src={check} />
                Prioridade SP com alternância entre SE e SG
              </li>
              <li>
                <img src={check} />
                Duas chamadas antes de registrar ausência
              </li>
            </ul>
          </div>
        </section>
        <section className="form-login">
          <div className="form-container">
            <span className="portal-atendente">PORTAL DO ATENDENTE</span>
            <h3>Acesse sua estação</h3>
            <p>Entre com suas credenciais para iniciar o atendimento.</p>
            <form className="login">
              <label htmlFor="email" className="email">
                E-mail institucional
                <input
                  type="email"
                  name="email"
                  id="email"
                  placeholder="seu.email@nassau.com.br"
                />
              </label>
              <label htmlFor="senha" className="senha">
                Senha
                <input
                  type="password"
                  name="senha"
                  id="senha"
                  placeholder="Digite sua senha"
                />
              </label>
              <div className="opcoes-acesso">
                <label htmlFor="manter-conectado" className="manter-conectado">
                  <input
                    type="checkbox"
                    name="manter-conectado"
                    id="manter-conectado"
                  />
                  Manter conectado
                </label>
                <span className="esqueci-senha">Esqueci minha senha</span>
              </div>
              <input type="submit" value="Entrar" className="submit" />
            </form>
          </div>
          <span className="acesso-exclusivo">
            Acesso exclusivo a colaboradores autorizados.
          </span>
        </section>
      </div>
    </>
  );
};

export default LoginAtendente;
