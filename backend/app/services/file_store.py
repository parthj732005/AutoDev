import os
import shutil
from app.db.session import SessionLocal
from app.db.models import GeneratedFile

# Where to store generated files
BASE_DIR = os.path.join(os.getcwd(), "generated_projects")


def save_project_files(
    project_name: str,
    story_id: str,
    agent_name: str,
    base_path: str
):
    """
    Saves generated project files both to filesystem and the database.
    File system is required for UI file browser and ZIP downloads.
    Database metadata is optional and used for history/logs.
    """

    # -----------------------------
    # 1. Save to filesystem
    # -----------------------------
    project_root = os.path.join(BASE_DIR, project_name)
    os.makedirs(project_root, exist_ok=True)

    for root, _, files in os.walk(base_path):
        for fname in files:
            src_full = os.path.join(root, fname)

            # Relative path inside project
            rel_path = os.path.relpath(src_full, base_path)
            dest_full = os.path.join(project_root, rel_path)

            # Ensure directories exist
            os.makedirs(os.path.dirname(dest_full), exist_ok=True)

            # Copy file
            shutil.copy2(src_full, dest_full)

    print(f"[PERSISTENCE] Saved files → {project_root}")

    # -----------------------------
    # 2. Save to database (optional)
    # -----------------------------
    db = SessionLocal()

    for root, _, files in os.walk(base_path):
        for fname in files:
            src_full = os.path.join(root, fname)

            with open(src_full, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            rel_path = os.path.relpath(src_full, base_path)

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
