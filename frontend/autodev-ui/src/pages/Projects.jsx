import { useState } from "react";
import { Link } from "react-router-dom";
import CreateProjectModal from "../components/CreateProjectModal";
import safeFetch from "../utils/safeFetch";


export default function Projects() {
  const [projects, setProjects] = useState([]);
  const [modalOpen, setModalOpen] = useState(false);

  const handleCreateProject = async (name) => {
    try {
      await safeFetch("http://localhost:8000/projects/create", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ project_name: name }),
      });

      setProjects(prev => [...prev, { id: name, name }]);
      setModalOpen(false);
    } catch {
      alert("Backend unreachable");
    }
  };

  return (
    <div>
      <button
        onClick={() => setModalOpen(true)}
        className="mb-4 px-4 py-2 bg-brand-primary text-white rounded"
      >
        + Create Project
      </button>

      <CreateProjectModal
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        onCreate={handleCreateProject}
      />

      <ul className="space-y-2">
        {projects.map(p => (
          <li key={p.id}>
            <Link to={`/projects/${p.id}`} className="text-blue-600">
              {p.name}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
