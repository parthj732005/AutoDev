import { createContext, useContext, useEffect, useState } from "react";

const BackendStatusContext = createContext();

const BACKEND_URL = "http://localhost:8000";

export function BackendStatusProvider({ children }) {
  const [reachable, setReachable] = useState(true);
  const [checking, setChecking] = useState(true);

  const checkBackend = async () => {
    setChecking(true);
    try {
      const res = await fetch(`${BACKEND_URL}/health`, {
        method: "GET",
      });

      setReachable(res.ok);
    } catch {
      setReachable(false);
    } finally {
      setChecking(false);
    }
  };

  useEffect(() => {
    checkBackend();
    const interval = setInterval(checkBackend, 15000); // every 15s
    return () => clearInterval(interval);
  }, []);

  return (
    <BackendStatusContext.Provider
      value={{ reachable, checking, refresh: checkBackend }}
    >
      {children}
    </BackendStatusContext.Provider>
  );
}

export const useBackendStatus = () => useContext(BackendStatusContext);
