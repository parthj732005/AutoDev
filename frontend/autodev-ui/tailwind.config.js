/** @type {import('tailwindcss').Config} */
export default {
  darkMode: "class",
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        /* ---------- Light theme ---------- */
        brand: {
          primary: "#2563eb",   // blue-600
          secondary: "#6366f1", // indigo-500
          muted: "#64748b",     // slate-500
          bg: "#f8fafc",        // slate-50
          panel: "#ffffff",     // white cards
          text: "#0f172a",      // slate-900 (added)
          border: "#e5e7eb",    // gray-200  (added)
        },

        /* ---------- Dark (soft cyberpunk) ---------- */
        cyber: {
          bg: "#0b0f1a",        // near-black blue
          panel: "#111827",     // gray-900
          border: "#1f2937",    // gray-800
          text: "#e5e7eb",      // gray-200
          accent: "#22d3ee",    // cyan-400
          glow: "#8b5cf6",      // violet-500
        },
      },

      boxShadow: {
        soft: "0 4px 30px rgba(0, 0, 0, 0.08)",
        cyber: "0 0 20px rgba(34, 211, 238, 0.15)",
      },

      animation: {
        fade: "fadeIn 0.25s ease-in-out",
        slide: "slideUp 0.3s ease-out",
        glow: "glowPulse 2.5s ease-in-out infinite",
      },

      keyframes: {
        fadeIn: {
          "0%": { opacity: "0" },
          "100%": { opacity: "1" },
        },
        slideUp: {
          "0%": { opacity: "0", transform: "translateY(8px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        glowPulse: {
          "0%, 100%": {
            boxShadow: "0 0 20px rgba(34, 211, 238, 0.2)",
          },
          "50%": {
            boxShadow: "0 0 32px rgba(139, 92, 246, 0.45)",
          },
        },
      },
    },
  },
  plugins: [],
};
