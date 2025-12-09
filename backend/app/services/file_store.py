import os
from app.db.session import SessionLocal
from app.db.models import GeneratedFile


def save_project_files(
    project_name: str,
    story_id: str,
    agent_name: str,
    base_path: str
):
    db = SessionLocal()

    for root, _, files in os.walk(base_path):
        for fname in files:
            full_path = os.path.join(root, fname)

            with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            rel_path = os.path.relpath(full_path, base_path)

            record = GeneratedFile(
                project_name=project_name,
                story_id=story_id,
                agent_name=agent_name,
                file_path=rel_path,
                language=fname.split(".")[-1],
                content=content,
            )

            db.add(record)

    db.commit()
    db.close()
