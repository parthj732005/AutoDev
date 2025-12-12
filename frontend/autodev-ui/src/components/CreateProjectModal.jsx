// src/components/CreateProjectModal.jsx
import { useState } from "react";

export default function CreateProjectModal({ open, onClose, onCreate }) {
  const [projectName, setProjectName] = useState("");
  const [loading, setLoading] = useState(false);

  if (!open) return null;

  const handleCreate = async () => {
    if (!projectName.trim()) return;

    setLoading(true);
    await onCreate(projectName.trim());
    setLoading(false);
    setProjectName("");
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm">
      <div className="w-full max-w-md rounded-xl p-6 bg-brand-panel dark:bg-cyber-panel shadow-soft">
        <h2 className="text-lg font-semibold mb-4">Create New Project</h2>

        <input
          type="text"
          placeholder="Project name"
          value={projectName}
          onChange={(e) => setProjectName(e.target.value)}
          className="w-full px-4 py-2 rounded-md mb-4 border bg-transparent"
        />

        <div className="flex justify-end gap-3">
          <button onClick={onClose} className="text-sm opacity-70">
            Cancel
          </button>

          <button
            onClick={handleCreate}
            disabled={loading}
            className="px-4 py-2 text-sm rounded-md bg-brand-primary text-white"
          >
            {loading ? "Creating…" : "Create"}
          </button>
        </div>
      </div>
    </div>
  );
}
