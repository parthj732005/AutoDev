import tempfile
import os
from app.services.backend_agent import BackendAgent
from app.services.frontend_agent import FrontendAgent
from app.services.db_agent import DatabaseAgent
from app.services.test_agent import TestAgent
from app.services.task_parser import detect_patterns
from app.services.task_decomposer import decompose_story
from app.services.file_store import save_project_files
from app.services.logger import log


# ------------------------
# Coordinator
# ------------------------
def coordinator_node(state):
    story = state["story"]
    title = story.get("title", "")
    desc = story.get("description", "")

    log("Coordinator: Starting task decomposition")
    log(f"Story → {title}")

    tasks = decompose_story(story)
    patterns = detect_patterns(title + " " + desc)
    workspace = tempfile.mkdtemp(prefix="autodev_")

    log(f"Coordinator: Detected tasks → {tasks}")
    log(f"Coordinator: Detected patterns → {patterns}")
    log(f"Workspace created → {workspace}")

    return {
        "detected_patterns": patterns,
        "tasks": tasks,
        "local_workspace": workspace,
    }


# ------------------------
# Backend Agent
# ------------------------
def backend_node(state):
    if "BACKEND" not in state["tasks"]:
        log("Backend Agent: Skipped (no backend task detected)")
        return {}

    log("Backend Agent: Generating backend API...")

    try:
        BackendAgent().generate_api(
            story=state["story"],
            project_name=state["project_name"],
            base_path=state["local_workspace"],
        )
        log("Backend Agent: Finished backend API generation")
    except Exception as e:
        log(f"❌ Backend Agent ERROR: {e}")
        return {}

    return {"backend_done": True}


# ------------------------
# Frontend Agent
# ------------------------
def frontend_node(state):
    if "FRONTEND" not in state["tasks"]:
        log("Frontend Agent: Skipped (no frontend task detected)")
        return {}

    log("Frontend Agent: Generating UI components...")

    try:
        FrontendAgent().generate_ui(
            story=state["story"],
            project_name=state["project_name"],
            base_path=state["local_workspace"],
        )
        log("Frontend Agent: Finished UI generation")
    except Exception as e:
        log(f"❌ Frontend Agent ERROR: {e}")
        return {}

    return {"frontend_done": True}


# ------------------------
# Database Agent
# ------------------------
def db_node(state):
    if "DATABASE" not in state["tasks"]:
        log("Database Agent: Skipped (no database task detected)")
        return {}

    log("Database Agent: Generating SQL schema...")

    try:
        DatabaseAgent().generate_schema(
            project_name=state["project_name"],
            base_path=state["local_workspace"],
        )
        log("Database Agent: Schema generation complete")
    except Exception as e:
        log(f"❌ Database Agent ERROR: {e}")
        return {}

    return {"db_done": True}


# ------------------------
# Test Agent + File Persistence
# ------------------------
def test_node(state):
    log("Test Agent: Generating test suite...")

    try:
        result = TestAgent().generate_tests(
            base_path=state["local_workspace"]
        )
        log("Test Agent: Test files created")
    except Exception as e:
        log(f"❌ Test Agent ERROR: {e}")
        result = {"status": "ERROR", "details": str(e)}

    # ------------------------
    # Persist project files
    # ------------------------
    try:
        log("Persistence: Saving generated files to project folder...")
        save_project_files(
            project_name=state["project_name"],
            story_id=str(state["story"].get("id", "unknown")),
            agent_name="system",
            base_path=state["local_workspace"],
        )
        log("Persistence: Files saved successfully")
    except Exception as e:
        log(f"❌ Persistence ERROR: {e}")

    return {
        "tests_done": True,
        "test_results": result,
        "test_status": result.get("status", "PASS"),
        "persisted": True,
    }
