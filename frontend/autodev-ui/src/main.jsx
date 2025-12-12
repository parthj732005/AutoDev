import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App.jsx";
import { ThemeProvider } from "./context/ThemeContext";
import { AuthProvider } from "./context/AuthContext";
import { BackendStatusProvider } from "./context/BackendStatusContext";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <AuthProvider>
      <BackendStatusProvider>
        <ThemeProvider>
          <App />
        </ThemeProvider>
      </BackendStatusProvider>
    </AuthProvider>
  </StrictMode>
);
