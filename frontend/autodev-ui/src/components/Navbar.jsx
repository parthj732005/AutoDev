// src/components/Navbar.jsx
import { useTheme } from "../context/ThemeContext";
import { useAuth } from "../context/AuthContext";

export default function Navbar() {
  const { theme, setTheme } = useTheme();
  const { user, logout } = useAuth();

  const email = user?.email || "guest@autodev.ai";

  return (
    <div className="flex justify-between items-center px-6 py-3 border-b dark:border-gray-800">
      <h1 className="font-bold text-lg">AutoDev</h1>

      <div className="flex items-center gap-4">
        <span className="text-sm">{email}</span>

        <button
          onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
          className="text-xs px-2 py-1 rounded border"
        >
          {theme === "dark" ? "Light" : "Dark"}
        </button>

        <button
          onClick={logout}
          className="text-red-500 text-sm"
        >
          Logout
        </button>
      </div>
    </div>
  );
}
