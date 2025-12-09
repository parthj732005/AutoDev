import { Link } from "react-router-dom";

export default function Home() {
    return (
        <div className="p-6">
            <h1 className="text-2xl font-bold">Welcome to AutoDev</h1>
            <p className="mt-2 text-gray-600">
                Automate software development using AI agents.
            </p>

            <div className="mt-6">
                <Link to="/projects" className="text-blue-600 underline">
                    Go to Projects
                </Link>
            </div>
        </div>
    );
}
