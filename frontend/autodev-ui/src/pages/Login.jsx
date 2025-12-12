import { useAuth } from "../context/AuthContext";
import { Navigate } from "react-router-dom";

export default function Login() {
  const { user, loginWithGoogle } = useAuth();

  if (user) return <Navigate to="/home" />;

  return (
    <div className="h-screen flex items-center justify-center bg-brand-bg dark:bg-cyber-bg">
      <div className="bg-brand-panel dark:bg-cyber-panel p-8 rounded-xl shadow-soft w-96 text-center space-y-6">

        <h1 className="text-2xl font-bold">Welcome to AutoDev</h1>

        <button
          onClick={loginWithGoogle}
          className="w-full py-2 bg-brand-primary text-white rounded
                     hover:opacity-90 flex items-center justify-center gap-2"
        >
          Continue with Google
        </button>

      </div>
    </div>
  );
}
