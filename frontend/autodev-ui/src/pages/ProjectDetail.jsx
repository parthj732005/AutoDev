import { useEffect, useRef, useState } from "react";
import { useParams } from "react-router-dom";
import safeFetch from "../utils/safeFetch";

export default function ProjectDetail() {
  const { id } = useParams(); // project_name

  const [org, setOrg] = useState("");
  const [adoProject, setAdoProject] = useState("");
  const [pat, setPat] = useState("");

  const [workItems, setWorkItems] = useState([]);
  const [loading, setLoading] = useState(false);

  const [logs, setLogs] = useState("");
  const logSourceRef = useRef(null);

  // -----------------------------
  // Fetch Azure DevOps work items
  // -----------------------------
  const fetchWorkItems = async () => {
    if (!org || !adoProject || !pat) {
      alert("Please fill all Azure DevOps fields");
      return;
    }

    setLoading(true);
    try {
      const res = await safeFetch(
        "http://localhost:8000/projects/ado/work-items",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ org, project: adoProject, pat }),
        }
      );

      const data = await res.json();
      setWorkItems(data || []);
    } catch {
      alert("Failed to fetch work items");
    } finally {
      setLoading(false);
    }
  };

  // -----------------------------
  // Run a selected work item
  // -----------------------------
  const runWorkItem = async (item) => {
    const normalizedStory = {
      title: item.title || item.name || item.type || "AutoDev Generated Task",
      description: item.description || "No description provided by Azure DevOps.",
    };

    setLogs("");
    startLogStream();

    try {
      await safeFetch("http://localhost:8000/projects/run", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          project_name: id,
          story: normalizedStory,
        }),
      });
    } catch {
      alert("Failed to run work item");
    }
  };



  // -----------------------------
  // Live log streaming (SSE)
  // -----------------------------
  const startLogStream = () => {
    if (logSourceRef.current) {
      logSourceRef.current.close();
    }

    const source = new EventSource("http://localhost:8000/logs/stream");
    logSourceRef.current = source;

    source.onmessage = (event) => {
      setLogs((prev) => prev + event.data + "\n");
    };

    source.onerror = () => {
      source.close();
      logSourceRef.current = null;
    };
  };


  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (logSourceRef.current) {
        logSourceRef.current.close();
      }
    };
  }, []);

  return (
    <div className="space-y-8">

      {/* ---------------- Azure DevOps Config ---------------- */}
      <div
        className="
          bg-brand-panel dark:bg-cyber-panel
          border border-brand-border dark:border-cyber-border
          text-brand-text dark:text-cyber-text
          p-5 rounded-xl space-y-3
        "
      >
        <h3 className="font-semibold text-lg">
          Azure DevOps Configuration
        </h3>

        <input
          value={org}
          onChange={(e) => setOrg(e.target.value)}
          placeholder="Organization name"
          className="
            w-full p-2 rounded
            bg-white dark:bg-cyber-bg
            text-brand-text dark:text-cyber-text
            border border-brand-border dark:border-cyber-border
          "
        />

        <input
          value={adoProject}
          onChange={(e) => setAdoProject(e.target.value)}
          placeholder="Project name"
          className="
            w-full p-2 rounded
            bg-white dark:bg-cyber-bg
            text-brand-text dark:text-cyber-text
            border border-brand-border dark:border-cyber-border
          "
        />

        <input
          type="password"
          value={pat}
          onChange={(e) => setPat(e.target.value)}
          placeholder="Personal Access Token (PAT)"
          className="
            w-full p-2 rounded
            bg-white dark:bg-cyber-bg
            text-brand-text dark:text-cyber-text
            border border-brand-border dark:border-cyber-border
          "
        />

        <button
          onClick={fetchWorkItems}
          disabled={loading}
          className="px-4 py-2 bg-brand-primary text-white rounded"
        >
          {loading ? "Fetching…" : "Fetch Work Items"}
        </button>
      </div>

      {/* ---------------- Work Items ---------------- */}
      <div
        className="
          bg-brand-panel dark:bg-cyber-panel
          border border-brand-border dark:border-cyber-border
          text-brand-text dark:text-cyber-text
          p-5 rounded-xl
        "
      >
        <h3 className="font-semibold text-lg mb-3">Work Items</h3>

        {workItems.length === 0 && (
          <p className="text-sm text-brand-muted dark:text-gray-400">
            No work items loaded
          </p>
        )}

        <ul className="space-y-2 text-sm">
          {workItems.map((item) => (
            <li
              key={item.id}
              className="
                flex justify-between items-center
                border-b border-brand-border dark:border-cyber-border
                pb-2
              "
            >
              <div>
                <p className="font-medium">{item.title}</p>
                <p className="opacity-60">{item.type}</p>
              </div>

              <button
                onClick={() => runWorkItem(item)}
                className="px-3 py-1 text-xs bg-green-600 text-white rounded"
              >
                Run
              </button>
            </li>
          ))}
        </ul>
      </div>

      {/* ---------------- Live Logs ---------------- */}
      {logs && (
        <div
          className="
            bg-black text-green-400
            dark:bg-black
            border border-brand-border dark:border-cyber-border
            p-4 rounded-xl
            font-mono text-xs
            max-h-72 overflow-y-auto
          "
        >
          <h3 className="text-sm font-semibold text-white mb-2">
            Live Execution Logs
          </h3>

          <pre className="whitespace-pre-wrap">
            {logs}
          </pre>
        </div>
      )}

    </div>
  );
}
