from typing import TypedDict, List, Dict, Any

class AgentState(TypedDict):
    story: dict
    project_name: str

    # planning
    detected_patterns: List[str]
    tasks: List[str]

    # execution
    local_workspace: str
    generated_files: Dict[str, str]

    # agents output
    backend_done: bool
    frontend_done: bool
    db_done: bool
    tests_done: bool

    test_results: Dict[str, Any]

    # feedback (used later)
    feedback: List[dict]
    refined_rules: Dict[str, Any]
