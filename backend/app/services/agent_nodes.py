import tempfile
from app.services.backend_agent import BackendAgent
from app.services.frontend_agent import FrontendAgent
from app.services.db_agent import DatabaseAgent
from app.services.test_agent import TestAgent
from app.services.task_parser import detect_patterns
from app.services.task_decomposer import decompose_story
from app.services.file_store import save_project_files


# ------------------------
# Coordinator
# ------------------------
def coordinator_node(state):
    story = state["story"]

    patterns = detect_patterns(
        story["title"] + " " + story.get("description", "")
    )
    tasks = decompose_story(story)

    state["detected_patterns"] = patterns
    state["tasks"] = tasks

    # ✅ temp workspace
    workspace = tempfile.mkdtemp(prefix="autodev_")
    state["local_workspace"] = workspace

    return state


# ------------------------
# Backend Agent Node
# ------------------------
def backend_node(state):
    if "BACKEND" not in state["tasks"]:
        return state

    BackendAgent().generate_api(
        story=state["story"],
        project_name=state["project_name"],
        base_path=state["local_workspace"]   # ✅ IMPORTANT
    )

    state["backend_done"] = True
    return state


# ------------------------
# Frontend Agent Node
# ------------------------
def frontend_node(state):
    if "FRONTEND" not in state["tasks"]:
        return state

    FrontendAgent().generate_ui(
        story=state["story"],
        project_name=state["project_name"],
        base_path=state["local_workspace"]   # ✅ IMPORTANT
    )

    state["frontend_done"] = True
    return state


# ------------------------
# Database Agent Node
# ------------------------
def db_node(state):
    if "DATABASE" not in state["tasks"]:
        return state

    DatabaseAgent().generate_schema(
        project_name=state["project_name"],
        base_path=state["local_workspace"]   # ✅ IMPORTANT
    )

    state["db_done"] = True
    return state


# ------------------------
# Testing + Persistence
# ------------------------
def test_node(state):
    if "TESTING" not in state["tasks"]:
        return state

    agent = TestAgent()

    result = agent.generate_tests(
        base_path=state["local_workspace"]
    )

    # ✅ Always normalize result
    status = result.get("status", "FAIL")

    state["tests_done"] = True
    state["test_results"] = result
    state["test_status"] = status

    # ✅ DEMO-SAFE GUARANTEE
    if status == "PASS":
        save_project_files(
            project_name=state["project_name"],
            story_id=str(state["story"].get("id", "unknown")),
            agent_name="system",
            base_path=state["local_workspace"],
        )

        state["persisted"] = True
    else:
        state["persisted"] = False

    return state
