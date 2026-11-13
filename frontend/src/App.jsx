import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import PainelPrincipal from "./apps/painel/PainelPrincipal";
import TotemHome from "./apps/totem/TotemHome";
import LoginAtendente from "./apps/atendente/LoginAtendente";
import Home from "./pages/Home";
import "./App.css";
import { NavigationProvider } from "./contexts/NavigationContext";

function App() {
  return (
    <BrowserRouter>
      <NavigationProvider>
        <Routes>
          {/* HOME */}
          <Route path="/" element={<Home />} />

          {/* PAINEL */}
          <Route path="/painel" element={<PainelPrincipal />} />

          {/* TOTEM */}
          <Route path="/totem" element={<TotemHome />} />

          {/* ATENDENTE */}
          <Route path="/atendente/login" element={<LoginAtendente />} />
        </Routes>
      </NavigationProvider>
    </BrowserRouter>
  );
}

export default App;
