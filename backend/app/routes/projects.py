from fastapi import APIRouter
from pydantic import BaseModel
import base64
import requests
from fastapi import HTTPException

router = APIRouter()


# -----------------------------
# Existing fake endpoints stay
# -----------------------------
FAKE_PROJECTS = [
    {"id": 1, "name": "Demo Project"},
    {"id": 2, "name": "Sample AutoDev Project"}
]

@router.get("/")
def get_projects():
    return FAKE_PROJECTS


# -----------------------------
# NEW Azure DevOps ingestion
# -----------------------------
class AzureProjectConfig(BaseModel):
    org: str
    project: str
    pat: str

from app.services.langgraph_coordinator import build_graph
from app.services.logger import log

graph = build_graph()

@router.post("/run")
def run_work_item(work_item: dict):
    state = {
        "story": work_item,
        "project_name": work_item.get("project_name", "default"),
        "feedback": [],
        "refined_rules": {}
    }

    log("LangGraph: execution started")
    graph.invoke(state)
    log("LangGraph: execution completed")

    return {"status": "completed"}
@router.post("/ado/work-items")
def get_ado_work_items(payload: dict):
    print("🔥🔥🔥 ADO ENDPOINT HIT 🔥🔥🔥")
    print("PAYLOAD:", payload)
    org = payload["org"]
    project = payload["project"]
    pat = payload["pat"]

    print("✅ ADO endpoint hit", org, project)

    auth = base64.b64encode(f":{pat}".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth}",
        "Content-Type": "application/json"
    }

    wiql_url = f"https://dev.azure.com/{org}/{project}/_apis/wit/wiql?api-version=7.0"
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
        f"https://dev.azure.com/{org}/{project}"
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
