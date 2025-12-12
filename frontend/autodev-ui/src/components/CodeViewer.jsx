import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneDark, oneLight } from "react-syntax-highlighter/dist/esm/styles/prism";
import { useTheme } from "../context/ThemeContext";

export default function CodeViewer({ code, language = "javascript" }) {
  const { theme } = useTheme();

  return (
    <div className="rounded-lg overflow-hidden border dark:border-cyber-border">
      <SyntaxHighlighter
        language={language}
        style={theme === "dark" ? oneDark : oneLight}
        customStyle={{
          margin: 0,
          fontSize: "0.85rem",
          background: "transparent",
        }}
        showLineNumbers
        wrapLongLines
      >
        {code}
      </SyntaxHighlighter>
    </div>
  );
}
