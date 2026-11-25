import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";

export default function RotaProtegida() {
  const { autenticado } = useAuth();

  return autenticado ? <Outlet /> : <Navigate to="/atendente/login" replace />;
}
