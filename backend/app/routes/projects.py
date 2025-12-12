from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import base64
import requests

from app.services.langgraph_coordinator import build_graph
from app.services.logger import log

router = APIRouter()

graph = build_graph()

# -----------------------------
# Fake project list (UI needs it)
# -----------------------------
@router.get("/")
def get_projects():
    return [
        {"id": 1, "name": "Demo Project"},
        {"id": 2, "name": "Sample AutoDev Project"}
    ]


# -----------------------------
# Azure DevOps config
# -----------------------------
class AzureProjectConfig(BaseModel):
    org: str
    project: str
    pat: str


# -----------------------------
# Azure DevOps work items (WIQL)
# -----------------------------
@router.post("/ado/work-items")
def get_ado_work_items(config: AzureProjectConfig):
    print("🔥 ADO ENDPOINT HIT", config.org, config.project)

    auth = base64.b64encode(f":{config.pat}".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth}",
        "Content-Type": "application/json"
    }

    wiql_url = (
        f"https://dev.azure.com/{config.org}/{config.project}"
        "/_apis/wit/wiql?api-version=7.0"
    )

    query = {
        "query": """
        SELECT [System.Id], [System.Title], [System.WorkItemType]
        FROM WorkItems
        ORDER BY [System.ChangedDate] DESC
        """
    }

    wiql_res = requests.post(wiql_url, headers=headers, json=query)
    wiql_res.raise_for_status()

    items = wiql_res.json().get("workItems", [])
    if not items:
        return []

    ids = ",".join(str(w["id"]) for w in items)

    items_url = (
        f"https://dev.azure.com/{config.org}/{config.project}"
        f"/_apis/wit/workitems?ids={ids}&api-version=7.0"
    )

    res = requests.get(items_url, headers=headers)
    res.raise_for_status()

    result = []
    for w in res.json()["value"]:
        f = w["fields"]
        result.append({
            "id": w["id"],
            "title": f.get("System.Title"),
            "type": f.get("System.WorkItemType"),
            "description": f.get("System.Description", "")
        })

    return result


# -----------------------------
# Run agent pipeline
# -----------------------------
@router.post("/run")
def run_work_item(payload: dict):
    story = payload.get("story")

    if not story or "title" not in story:
        raise HTTPException(400, "story with title is required")

    state = {
        "story": story,                      
        "project_name": payload.get("project_name", "default"),
        "feedback": [],
        "refined_rules": {}
    }

    log("LangGraph: execution started")
    graph.invoke(state)
    log("LangGraph: execution completed")

    return {"status": "completed"}

