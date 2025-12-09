from langgraph.graph import StateGraph
from app.services.agent_state import AgentState
from app.services.agent_nodes import (
    coordinator_node,
    backend_node,
    frontend_node,
    db_node,
    test_node,
)

def build_graph():
    graph = StateGraph(AgentState)

    # nodes
    graph.add_node("coordinator", coordinator_node)
    graph.add_node("backend", backend_node)
    graph.add_node("frontend", frontend_node)
    graph.add_node("database", db_node)
    graph.add_node("testing", test_node)

    # flow
    graph.set_entry_point("coordinator")

    # parallel execution
    graph.add_edge("coordinator", "backend")
    graph.add_edge("coordinator", "frontend")
    graph.add_edge("coordinator", "database")

    # all must finish before testing
    graph.add_edge("backend", "testing")
    graph.add_edge("frontend", "testing")
    graph.add_edge("database", "testing")

    graph.set_finish_point("testing")

    return graph.compile()
