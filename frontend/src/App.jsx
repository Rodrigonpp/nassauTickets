import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import PainelPrincipal from "./apps/painel/PainelPrincipal";
import TotemHome from "./apps/totem/TotemHome";
import LoginAtendente from "./apps/atendente/LoginAtendente";
import SelecaoPerfil from "./pages/SelecaoPerfil";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* HOME */}
        <Route path="/" element={<SelecaoPerfil />} />

        {/* PAINEL */}
        <Route path="/painel" element={<PainelPrincipal />} />

        {/* TOTEM */}
        <Route path="/totem" element={<TotemHome />} />

        {/* ATENDENTE */}
        <Route path="/atendente/login" element={<LoginAtendente />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
