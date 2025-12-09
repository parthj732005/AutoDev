import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";

export default function ProjectDetail() {
    const { id } = useParams();

    const [org, setOrg] = useState("");
    const [project, setProject] = useState("");
    const [pat, setPat] = useState("");
    const [workItems, setWorkItems] = useState([]);
    const [logs, setLogs] = useState([]);

    // ✅ Fetch Azure DevOps work items
    async function fetchWorkItems() {
        const res = await fetch(
            "http://127.0.0.1:8000/projects/ado/work-items",
            {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ org, project, pat })
            }
        );

        const data = await res.json();
        setWorkItems(data);
    }

    // ✅ Live log streaming (SSE)
    useEffect(() => {
        const evtSource = new EventSource(
            "http://127.0.0.1:8000/logs/stream"
        );

        evtSource.onmessage = (event) => {
            setLogs(prev => [...prev, event.data]);
        };

        return () => evtSource.close();
    }, []);

    return (
        <div className="p-6 space-y-4">
            <h2 className="text-xl font-bold">Project #{id}</h2>

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

            {/* Work Items List */}
            <ul className="space-y-2">
                {workItems.map(w => (
                    <li key={w.id} className="border p-3 rounded space-y-2">
                        <div className="font-semibold">{w.title}</div>
                        <div className="text-sm text-gray-600">{w.type}</div>

                        {/* ✅ RUN BUTTON (PHASE 3+) */}
                        <button
                            className="mt-2 px-3 py-1 bg-blue-600 text-white rounded"
                            onClick={() => {
                                fetch("http://127.0.0.1:8000/projects/run", {
                                    method: "POST",
                                    headers: { "Content-Type": "application/json" },
                                    body: JSON.stringify({
                                        id: w.id,
                                        title: w.title,
                                        description: w.description || "",
                                        project_name: project
                                    })
                                });
                            }}
                        >
                            Run
                        </button>
                    </li>
                ))}
            </ul>

            {/* ✅ LIVE LOGS */}
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
