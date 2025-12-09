import { useNavigate } from "react-router-dom";

export default function Login() {
    const navigate = useNavigate();

    return (
        <div className="h-screen flex items-center justify-center">
            <button
                className="px-6 py-3 bg-black text-white rounded"
                onClick={() => navigate("/home")}
            >
                Login with GitHub
            </button>
        </div>
    );
}
