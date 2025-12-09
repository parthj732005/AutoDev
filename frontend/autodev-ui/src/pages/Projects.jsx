import { Link } from "react-router-dom";

const projects = [
    { id: 1, name: "Demo Project" },
    { id: 2, name: "Sample AutoDev Project" }
];

export default function Projects() {
    return (
        <div className="p-6">
            <h2 className="text-xl font-bold">Projects</h2>

            <ul className="mt-4">
                {projects.map(p => (
                    <li key={p.id}>
                        <Link className="text-blue-600" to={`/projects/${p.id}`}>
                            {p.name}
                        </Link>
                    </li>
                ))}
            </ul>
        </div>
    );
}
