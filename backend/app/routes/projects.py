from fastapi import APIRouter
from pydantic import BaseModel
from app.services.azure_devops import AzureDevOpsClient

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


@router.post("/ado/work-items")
def fetch_work_items(config: AzureProjectConfig):
    client = AzureDevOpsClient(
        org=config.org,
        project=config.project,
        pat=config.pat
    )

    work_items = client.get_work_items()

    return [
        {
            "id": item["id"],
            "type": item["fields"]["System.WorkItemType"],
            "title": item["fields"]["System.Title"],
            "description": item["fields"].get("System.Description", "")
        }
        for item in work_items
    ]

from app.services.coordinator import Coordinator
from app.services.logger import log

@router.post("/run")
def run_work_item(work_item: dict):
    project_name = work_item.get("project_name", "Default Project")
    coordinator = Coordinator(logger=log)
    coordinator.run(work_item, project_name)
    return {"status": "started"}

