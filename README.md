---

# AutoDev: AI-Powered Full-Stack Project Generator

**AutoDev** is an intelligent platform designed to accelerate software development by autonomously generating full-stack project scaffolds.
By leveraging AI agents orchestrated with **LangGraph**, AutoDev takes user stories or Azure DevOps work items and converts them into runnable backend APIs, frontend UIs, database schemas, and test suites.

---

## 🚀 Features

### 🧠 AI Agent Orchestration

* Uses **LangGraph** to coordinate multiple specialized agents:

  * Coordinator
  * Backend Agent
  * Frontend Agent
  * Database Agent
  * Testing Agent
* Enables structured, multi-step reasoning for complex development tasks.

### 🛠 Automated Code Generation

* **Backend**

  * FastAPI endpoints
  * Pydantic request/response models
* **Frontend**

  * React components (Vite)
  * Styled with Tailwind CSS
* **Database**

  * SQL schemas (PostgreSQL dialect)
* **Testing**

  * Minimal `pytest` test suites for validation

### 🔗 Azure DevOps Integration

* Fetches work items and user stories directly from Azure DevOps using PAT authentication.

### 📡 Live Execution Logs

* Streams real-time agent logs to the UI using **Server-Sent Events (SSE)**.

### 📁 Project Management

* Create and manage multiple projects
* Browse generated file content directly in the UI

### 📦 Export & Persistence

* Download generated projects as a `.zip`
* Code is saved to:

  * Local filesystem
  * SQLite database (via SQLAlchemy)

---

## 🛠 Tech Stack

### Backend

* **Language**: Python 3.10+
* **Framework**: FastAPI
* **AI / LLM**: OpenAI API (`gpt-4o-mini`)
* **Orchestration**: LangGraph
* **Database**: SQLite (SQLAlchemy)
* **Utilities**: `uvicorn`, `pydantic`, `requests`

### Frontend

* **Framework**: React (Vite)
* **Styling**: Tailwind CSS
* **Authentication**: Firebase Auth
* **Routing**: React Router

---

## 📋 Prerequisites

Before running the project, ensure you have:

* Python 3.10 or higher
* Node.js and npm
* An OpenAI API key
* A Firebase project (for authentication)

---

## ⚙️ Installation & Setup

### 1️⃣ Backend Setup

1. Navigate to the backend directory:

```bash
cd backend
```

2. Create and activate a virtual environment (recommended):

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

> Ensure `langgraph`, `sqlalchemy`, and `openai` are installed.

4. Set environment variables:

* Add your OpenAI key:

```bash
export OPENAI_API_KEY=your_key_here
```

or create a `.env` file.

5. Run the backend server:

```bash
uvicorn app.main:app --reload
```

Backend will be available at:
👉 `http://localhost:8000`

---

### 2️⃣ Frontend Setup

1. Navigate to the frontend directory:

```bash
cd frontend/autodev-ui
```

2. Install dependencies:

```bash
npm install
```

3. Configure Firebase:

* Open `src/auth/firebase.js`
* Replace `firebaseConfig` with your Firebase project credentials

4. Start the development server:

```bash
npm run dev
```

Frontend will be available at:
👉 `http://localhost:5173`

---

## 📖 Usage Guide

1. **Login**

   * Open the frontend
   * Sign in using Google (Firebase Auth)

2. **Create Project**

   * Click **+ Create Project**
   * Provide a project name (e.g., `ProjectAlpha`)

3. **Fetch Work Items**

   * Open the project detail page
   * Enter:

     * Azure DevOps Organization
     * Project Name
     * Personal Access Token (PAT)
   * Click **Fetch Work Items**

4. **Run Agents**

   * Select a work item or story
   * Click **Run**
   * Watch real-time execution logs as agents generate code

---

## 📂 Project Structure

```text
AutoDev/
├── backend/
│   ├── app/
│   │   ├── db/              # Database models and session setup
│   │   ├── routes/          # API routes (projects, logs, files)
│   │   ├── services/        # AI agents and coordinator logic
│   │   ├── logs/            # Runtime execution logs
│   │   └── main.py          # FastAPI entry point
│   ├── generated_projects/  # AI-generated project outputs
│   └── autodev.db           # SQLite database
│
└── frontend/autodev-ui/
    ├── src/
    │   ├── auth/            # Firebase authentication
    │   ├── components/      # UI components
    │   ├── context/         # React contexts
    │   ├── layouts/         # Layout wrappers
    │   ├── pages/           # App pages
    │   └── utils/           # API helpers
    └── package.json
```

---

## 🤖 How It Works

1. **Input**

   * User provides a story (Title + Description)

2. **Coordinator Agent**

   * Detects patterns (CRUD, Auth, etc.)
   * Decomposes the story into tasks

3. **Specialized Agents**

   * **Backend Agent** → `api.py` (FastAPI)
   * **Database Agent** → `schema.sql`
   * **Frontend Agent** → `Generated.jsx`
   * **Test Agent** → `test_basic.py`

4. **Persistence**

   * Generated files are stored in:

     * `generated_projects/`
     * SQLite database for indexing and retrieval

---

If you want, I can next:

* Make this **hackathon-ready**
* Shorten it to a **1-page submission**
* Convert it into a **pitch deck**
* Improve wording to sound more **research-grade / academic**

Just tell me.
