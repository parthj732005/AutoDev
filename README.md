#AutoDev: AI-Powered Full-Stack Project Generator**AutoDev** is an intelligent platform designed to accelerate software development by autonomously generating full-stack project scaffolds. By leveraging AI agents orchestrated with LangGraph, AutoDev takes user stories or Azure DevOps work items and converts them into runnable backend APIs, frontend UIs, database schemas, and test suites.

##🚀 Features* **AI Agent Orchestration**: Uses **LangGraph** to coordinate multiple specialized agents (Coordinator, Backend, Frontend, Database, Testing) to complete complex development tasks.
* **Automated Code Generation**:
* **Backend**: Generates FastAPI endpoints with Pydantic models.
* **Frontend**: Creates functional React components styled with Tailwind CSS.
* **Database**: Produces SQL schemas (PostgreSQL dialect) for data persistence.
* **Tests**: Writes minimal `pytest` test suites to ensure basic functionality.


* **Azure DevOps Integration**: Connects to Azure DevOps to fetch work items and stories directly into the workflow.
* **Live Execution Logs**: Streams real-time logs from the AI agents to the UI via Server-Sent Events (SSE).
* **Project Management**: Create, manage, and view generated file content for multiple projects.
* **Export**: Download the entire generated project as a `.zip` file.
* **File Persistence**: generated code is saved to both the local filesystem and a SQLite database.

##🛠️ Tech Stack###Backend* **Language**: Python 3.10+
* **Framework**: FastAPI
* **AI/LLM**: OpenAI API (`gpt-4o-mini`)
* **Orchestration**: LangGraph
* **Database**: SQLite (via SQLAlchemy)
* **Utilities**: `uvicorn`, `pydantic`, `requests`

###Frontend* **Framework**: React (Vite)
* **Styling**: Tailwind CSS
* **Authentication**: Firebase Auth
* **Routing**: React Router

---

##📋 PrerequisitesBefore running the project, ensure you have the following installed:

* Python 3.10 or higher
* Node.js and npm
* An OpenAI API Key
* A Firebase project (for authentication)

---

##⚙️ Installation & Setup###1. Backend Setup1. Navigate to the backend directory:
```bash
cd backend

```


2. Create and activate a virtual environment (optional but recommended):
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

```


3. Install dependencies:
```bash
pip install -r requirenments.txt

```


*(Note: Ensure `langgraph`, `sqlalchemy`, and `openai` are installed if not present in the txt file)*
4. Set up environment variables:
* Set your `OPENAI_API_KEY` in your environment variables or create a `.env` file.


5. Initialize the database and run the server:
```bash
uvicorn app.main:app --reload

```


The backend API will be available at `http://localhost:8000`.

###2. Frontend Setup1. Navigate to the frontend directory:
```bash
cd frontend/autodev-ui

```


2. Install dependencies:
```bash
npm install

```


3. Configure Firebase:
* Open `src/auth/firebase.js`.
* Replace the empty `firebaseConfig` object with your actual Firebase project configuration keys.


4. Run the development server:
```bash
npm run dev

```


The UI will be available at `http://localhost:5173`.

---

##📖 Usage Guide1. **Login**: Open the frontend application. You can log in using Google (configured via Firebase).
2. **Create Project**: Click on **"+ Create Project"** to initialize a new workspace (e.g., "ProjectAlpha").
3. **Fetch Work Items**:
* Navigate to the project detail page.
* Enter your Azure DevOps **Organization**, **Project**, and **Personal Access Token (PAT)**.
* Click "Fetch Work Items" to load your backlog.


4. **Run Agents**:
* Select a work item (or story) from the list and click **"Run"**.
* Watch the **Live Execution Logs** panel as the agents analyze the story, generate code for backend/frontend/DB, and run tests.


5. **View & Download**:
* Once completed, you can browse the generated file structure in the UI.
* Click the **Download Zip** button (if implemented in UI) or check the `backend/generated_projects/` folder on your disk for the source code.



---

##📂 Project Structure```text
AutoDev/
├── backend/
│   ├── app/
│   │   ├── db/             # Database models and session setup
│   │   ├── routes/         # API endpoints (auth, projects, logs, files)
│   │   ├── services/       # AI Agents (Backend, Frontend, DB, Test, Coordinator)
│   │   ├── logs/           # Runtime logs
│   │   └── main.py         # App entry point
│   ├── generated_projects/ # Output directory for AI-generated code
│   └── autodev.db          # SQLite database
│
└── frontend/autodev-ui/
    ├── src/
    │   ├── auth/           # Firebase configuration
    │   ├── components/     # UI components (Navbar, CodeViewer, etc.)
    │   ├── context/        # React Contexts (Auth, Theme, BackendStatus)
    │   ├── layouts/        # App layout wrappers
    │   ├── pages/          # Main pages (Login, Home, Projects)
    │   └── utils/          # API fetch utilities
    └── package.json

```

##🤖 How It Works1. **Input**: The user provides a "Story" (Title + Description).
2. **Coordinator Agent**: Analyzes the story, detects patterns (Auth, CRUD, etc.), and decomposes it into tasks.
3. **Specialized Agents**:
* **Backend Agent**: Writes `api.py` using FastAPI.
* **Database Agent**: Writes `schema.sql`.
* **Frontend Agent**: Writes `Generated.jsx`.
* **Test Agent**: Writes `test_basic.py`.


4. **Persistence**: Files are saved to the `generated_projects` directory and indexed in the database.

---
