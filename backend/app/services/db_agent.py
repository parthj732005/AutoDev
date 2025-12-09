import os
from app.services.llm_client import call_llm

class DatabaseAgent:
    def generate_schema(self, project_name, base_path, entity="users"):
        prompt = f"""
Generate a PostgreSQL SQL schema.

Entity: {entity}

Rules:
- Use PostgreSQL syntax
- Primary key required
- Add email/password columns if auth-related
- Output SQL ONLY
"""

        sql = call_llm(prompt, max_tokens=400)

        base = os.path.join(base_path, "database")
        os.makedirs(base, exist_ok=True)

        path = os.path.join(base, f"{entity}.sql")
        with open(path, "w", encoding="utf-8") as f:
            f.write(sql)

        return {"status": "OK", "file": path}
