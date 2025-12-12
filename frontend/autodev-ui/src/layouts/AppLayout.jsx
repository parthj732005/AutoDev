// src/layouts/AppLayout.jsx
import { useAuth } from "../context/AuthContext";
import { Navigate } from "react-router-dom";
import Navbar from "../components/Navbar";

export default function AppLayout({ children }) {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-brand-bg dark:bg-cyber-bg">
        <span className="text-sm opacity-70">Loading…</span>
      </div>
    );
  }

  if (!user) {
    return <Navigate to="/" replace />;
  }

  return (
    <div className="min-h-screen bg-brand-bg dark:bg-cyber-bg text-gray-900 dark:text-cyber-text">
      <Navbar />
      <div className="p-6">{children}</div>
    </div>
  );
}
