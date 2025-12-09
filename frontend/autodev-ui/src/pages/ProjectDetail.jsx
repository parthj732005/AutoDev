import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";

export default function ProjectDetail() {
    const { id } = useParams();

    const [org, setOrg] = useState("");
    const [project, setProject] = useState("");
    const [pat, setPat] = useState("");
    const [workItems, setWorkItems] = useState([]);
    const [logs, setLogs] = useState([]);

    const [files, setFiles] = useState({});
    const [selectedFile, setSelectedFile] = useState(null);

    const [running, setRunning] = useState(false);

    // ✅ DEBUG STATE
    const [debug, setDebug] = useState("");

    // ------------------------
    // Fetch Azure DevOps work items
    // ------------------------
    async function fetchWorkItems() {
        try {
            setDebug("Fetching work items...");
            console.log("FETCH /ado/work-items", { org, project });

            const res = await fetch(
                "http://127.0.0.1:8000/projects/ado/work-items",
                {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ org, project, pat })
                }
            );

            setDebug(`Response status: ${res.status}`);

            const data = await res.json();
            console.log("WORK ITEMS RESPONSE:", data);

            if (!Array.isArray(data)) {
                setDebug("❌ Backend returned error. Check backend logs.");
                setWorkItems([]);
                return;
            }

            setDebug(`✅ Loaded ${data.length} work items`);
            setWorkItems(data);
        } catch (err) {
            console.error(err);
            setDebug("❌ Failed to fetch work items");
        }
    }

    // ------------------------
    // Fetch generated files
    // ------------------------
    async function fetchFiles() {
        if (!project) return;

        try {
            const res = await fetch(`http://127.0.0.1:8000/files/${project}`);
            const data = await res.json();
            setFiles(data || {});
        } catch {
            setFiles({});
        }
    }

    // ------------------------
    // SSE log streaming
    // ------------------------
    useEffect(() => {
        const evtSource = new EventSource(
            "http://127.0.0.1:8000/logs/stream"
        );

        evtSource.onmessage = (event) => {
            setLogs(prev => [...prev.slice(-200), event.data]);
        };

        evtSource.onerror = () => {
            setLogs(prev => [...prev, "❌ Log stream disconnected"]);
        };

        return () => evtSource.close();
    }, []);

    // Refresh files when project changes
    useEffect(() => {
        fetchFiles();
    }, [project]);

    return (
        <div className="p-6 space-y-4">
            <h2 className="text-xl font-bold">Project #{id}</h2>

            {/* ✅ DEBUG INFO */}
            {debug && (
                <div className="p-2 bg-yellow-100 text-sm rounded">
                    {debug}
                </div>
            )}

            {/* Azure DevOps Inputs */}
            <input
                className="border p-2 w-full"
                placeholder="Azure Org"
                value={org}
                onChange={e => setOrg(e.target.value)}
            />

            <input
                className="border p-2 w-full"
                placeholder="Project Name"
                value={project}
                onChange={e => setProject(e.target.value)}
            />

            <input
                className="border p-2 w-full"
                type="password"
                placeholder="Azure DevOps PAT"
                value={pat}
                onChange={e => setPat(e.target.value)}
            />

            <button
                className="bg-green-600 text-white px-4 py-2 rounded"
                onClick={fetchWorkItems}
            >
                Fetch Work Items
            </button>

            {/* ✅ WORK ITEMS COUNT */}
            <div className="text-sm text-gray-500">
                Work items loaded: {workItems.length}
            </div>

            {/* Work Items */}
            <ul className="space-y-2">
                {workItems.map(w => (
                    <li key={w.id} className="border p-3 rounded space-y-2">
                        <div className="font-semibold">{w.title}</div>
                        <div className="text-sm text-gray-600">{w.type}</div>

                        <button
                            disabled={running}
                            className={`mt-2 px-3 py-1 rounded text-white ${running
                                    ? "bg-gray-400 cursor-not-allowed"
                                    : "bg-blue-600"
                                }`}
                            onClick={async () => {
                                setRunning(true);
                                setDebug(`Running work item ${w.id}...`);

                                await fetch(
                                    "http://127.0.0.1:8000/projects/run",
                                    {
                                        method: "POST",
                                        headers: {
                                            "Content-Type": "application/json"
                                        },
                                        body: JSON.stringify({
                                            id: w.id,
                                            title: w.title,
                                            description: w.description || "",
                                            project_name: project
                                        })
                                    }
                                );

                                setTimeout(() => {
                                    fetchFiles();
                                    setRunning(false);
                                    setDebug("✅ Execution finished");
                                }, 1500);
                            }}
                        >
                            {running ? "Running..." : "Run"}
                        </button>
                    </li>
                ))}
            </ul>

            {/* ✅ FILE VIEWER */}
            <div className="mt-6">
                <h3 className="font-semibold">Generated Files</h3>

                {Object.entries(files).map(([path, f]) => (
                    <div
                        key={f.id}
                        className="cursor-pointer text-blue-500 hover:underline"
                        onClick={async () => {
                            const r = await fetch(
                                `http://127.0.0.1:8000/files/content/${f.id}`
                            );
                            setSelectedFile(await r.json());
                        }}
                    >
                        {path}
                    </div>
                ))}
            </div>

            {/* File content */}
            {selectedFile && (
                <pre className="bg-black text-green-400 p-3 mt-3 h-64 overflow-auto text-sm rounded">
                    {selectedFile.content}
                </pre>
            )}

            {/* ZIP download */}
            {project && (
                <a
                    href={`http://127.0.0.1:8000/download/${project}`}
                    className="inline-block mt-4 bg-purple-600 text-white px-4 py-2 rounded"
                >
                    Download ZIP
                </a>
            )}

            {/* Live logs */}
            <div className="mt-6 p-4 bg-black text-green-400 h-52 overflow-auto text-sm rounded">
                <div className="font-bold text-white mb-2">
                    Live Execution Logs
                </div>

                {logs.map((l, i) => (
                    <div key={i}>{l}</div>
                ))}
            </div>
        </div>
    );
}
