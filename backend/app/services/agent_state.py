from typing import TypedDict, List, Dict, Any, Annotated
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    story: Annotated[dict, "single"]

    project_name: str

    detected_patterns: List[str]
    tasks: List[str]

    local_workspace: str

    backend_done: bool
    frontend_done: bool
    db_done: bool
    tests_done: bool

    test_results: Dict[str, Any]
    feedback: List[dict]
    refined_rules: Dict[str, Any]