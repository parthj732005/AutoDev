import { Link } from "react-router-dom";
export default function Home() {
    return (
        <div className="p-6">
            <h1 className="text-2xl font-bold">Welcome to AutoDev</h1>
            <p className="mt-2 text-gray-600">
            AutoDev generates full-stack project scaffolds using AI agents.
            </p>
            <ul className="mt-4 text-sm text-gray-500 list-disc ml-5 space-y-1">
            <li>Create a project</li>
            <li>Connect Azure DevOps (optional)</li>
            <li>Select one or more work items</li>
            <li>Run agents to generate backend, frontend, and tests</li>
            </ul>

            <p className="mt-4 text-sm text-gray-500">
            Generated code is a runnable scaffold. Database and environment
            configuration should be completed by the user.
            </p>
            <p className="mt-4 text-sm text-gray-500">
            <strong>How to run the generated project:</strong>
            </p>

            <ol className="mt-2 text-sm text-gray-500 list-decimal ml-5 space-y-1">
            <li>Go to the generated project folder.</li>
            <li>Start the backend server (FastAPI).</li>
            <li>Start the frontend development server.</li>
            <li>Open the frontend in your browser.</li>
            </ol>

            <p className="mt-2 text-xs text-gray-400">
            Note: Database setup, environment variables, and production configuration
            are intentionally left to the user.
            </p>


            <div className="mt-6">
                <Link to="/projects" className="text-blue-600 underline">
                    Go to Projects
                </Link>
            </div>
        </div>
    );
}
