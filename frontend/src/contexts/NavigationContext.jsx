import { createContext, useContext } from "react";
import { useLocation } from "react-router-dom";

const NavigationContext = createContext();

export function NavigationProvider({ children }) {
  const location = useLocation();

  const getCurrentScreen = (pathname) => {
    if (pathname.startsWith("/painel")) return "painel";
    if (pathname.startsWith("/totem")) return "totem";
    if (pathname.startsWith("/atendente")) return "atendente";
    return "home";
  };

  const currentScreen = getCurrentScreen(location.pathname);

  return (
    <NavigationContext.Provider
      value={{ currentScreen, pathname: location.pathname }}
    >
      {children}
    </NavigationContext.Provider>
  );
}

export function useNavigation() {
  const context = useContext(NavigationContext);

  if (!context) {
    throw new Error(
      "useNavigation deve ser usado dentro de um NavigationProvider",
    );
  }

  return context;
}
