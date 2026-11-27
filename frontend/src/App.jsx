import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import PainelPrincipal from "./apps/painel/PainelPrincipal";
import TotemHome from "./apps/totem/TotemHome";
import LoginAtendente from "./apps/atendente/LoginAtendente";
import Home from "./pages/Home";
import "./App.css";
import { NavigationProvider } from "./contexts/NavigationContext";
import { ThemeProvider } from "./contexts/ThemeContext";
import DashboardAtendente from "./apps/atendente/DashboardAtendente";
import { AuthProvider } from "./contexts/AuthContext";
import RotaProtegida from "./components/RotaProtegida";

function App() {
  return (
    <BrowserRouter>
      <NavigationProvider>
        <ThemeProvider>
          <AuthProvider>
            <Routes>
              {/* HOME */}
              <Route path="/" element={<Home />} />

              {/* PAINEL */}
              <Route path="/painel" element={<PainelPrincipal />} />

              {/* TOTEM */}
              <Route path="/totem" element={<TotemHome />} />

              {/* ATENDENTE */}
              <Route path="/atendente">
                <Route path="login" element={<LoginAtendente />} />

                <Route element={<RotaProtegida />}>
                  <Route path="dashboard" element={<DashboardAtendente />} />
                </Route>
              </Route>
            </Routes>
          </AuthProvider>
        </ThemeProvider>
      </NavigationProvider>
    </BrowserRouter>
  );
}

export default App;
