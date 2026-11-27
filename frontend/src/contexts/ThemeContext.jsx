import { createContext, useContext, useEffect, useState } from "react";
import { useNavigation } from "./NavigationContext";

const ThemeContext = createContext();

export function ThemeProvider({ children }) {
  const { currentScreen } = useNavigation();
  const [theme, setTheme] = useState("light");

  useEffect(() => {
    if (currentScreen === "painel") {
      setTheme("dark");
    } else {
      setTheme("light");
    }
  }, [currentScreen]);

  return (
    <ThemeContext.Provider value={{ theme }}>{children}</ThemeContext.Provider>
  );
}

export function useTheme() {
  const context = useContext(ThemeContext);

  if (!context) {
    throw new Error("useTheme deve ser usado dentro de um ThemeProvider");
  }

  return context;
}
