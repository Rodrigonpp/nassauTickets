import React, { useState } from "react";
import Header from "../../components/Header";
import safety_shield from "../../assets/safety_shield.svg";
import check from "../../assets/check.svg";
import "./LoginAtendente.css";
import { Navigate, useNavigate } from "react-router-dom";
import { useLogin } from "../../hooks/useLogin";
import { useAuth } from "../../contexts/AuthContext";

const LoginAtendente = () => {
  const navigate = useNavigate();
  const { autenticado } = useAuth();
  const { autenticar, loading, erro } = useLogin();

  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [manterConectado, setManterConectado] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    const sucesso = await autenticar({
      login: email,
      senha,
      manterConectado,
    });

    if (sucesso) {
      navigate("/atendente/dashboard", { replace: true });
    }
  };

  if (autenticado) {
    return <Navigate to="/atendente/dashboard" replace />;
  }
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
            <form className="login" onSubmit={handleSubmit}>
              <label htmlFor="email" className="email">
                E-mail institucional
                <input
                  type="email"
                  name="email"
                  id="email"
                  placeholder="seu.email@nassau.com.br"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  autoComplete="username"
                  required
                />
              </label>
              <label htmlFor="senha" className="senha">
                Senha
                <input
                  type="password"
                  name="senha"
                  id="senha"
                  placeholder="Digite sua senha"
                  value={senha}
                  onChange={(e) => setSenha(e.target.value)}
                  autoComplete="current-password"
                  required
                />
              </label>
              <div className="opcoes-acesso">
                <label htmlFor="manter-conectado" className="manter-conectado">
                  <input
                    type="checkbox"
                    name="manter-conectado"
                    id="manter-conectado"
                    checked={manterConectado}
                    onChange={(e) => setManterConectado(e.target.checked)}
                  />
                  Manter conectado
                </label>
                <span className="esqueci-senha">Esqueci minha senha</span>
              </div>
              {erro && (
                <p className="erro-login" role="alert">
                  {erro}
                </p>
              )}
              <input
                type="submit"
                value={loading ? "Entrando..." : "Entrar"}
                className="submit"
                disabled={loading}
              />
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
