import os
import json
import zipfile
import io
from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import StreamingResponse

from app.db.session import SessionLocal
from app.db.models import GeneratedFile

router = APIRouter(prefix="/files")

BASE_GENERATED_DIR = os.path.join(
    os.getcwd(),
    "backend", 
    "generated_projects"
)

# ---------------------------------------------
# READ SINGLE FILE CONTENT
# ---------------------------------------------
@router.get("/content")
def read_file(path: str, project: str):
    """
    Load generated file content either from DB or disk.
    """
    db = SessionLocal()
    
    record = (
        db.query(GeneratedFile)
        .filter(
            GeneratedFile.project_name == project,
            GeneratedFile.file_path == path
        )
        .first()
    )
    
    db.close()

    if not record:
        raise HTTPException(404, "File not found in DB")

    return {
        "path": path,
        "content": record.content
    }


# ---------------------------------------------
# LIST ALL FILES FOR A PROJECT
# ---------------------------------------------
@router.get("/{project_name}")
def list_files(project_name: str):
    db = SessionLocal()

    files = (
        db.query(GeneratedFile)
        .filter(GeneratedFile.project_name == project_name)
        .all()
    )

    db.close()

    if not files:
        return {}

    output = {}

    for f in files:
        output[f.file_path] = {
            "id": f.id,
            "language": f.language,
        }

    return output


# ---------------------------------------------
# DOWNLOAD FULL ZIP OF GENERATED PROJECT
# ---------------------------------------------
@router.get("/download/{project_name}")
def download_project_zip(project_name: str):

    project_folder = os.path.join(BASE_GENERATED_DIR, project_name)

    if not os.path.exists(project_folder):
        raise HTTPException(404, "Project folder not found")

    # Create in-memory zip
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(project_folder):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, project_folder)
                zipf.write(full_path, rel_path)

    zip_buffer.seek(0)

    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={
            "Content-Disposition": f"attachment; filename={project_name}.zip"
        },
    )
