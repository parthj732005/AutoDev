import os
from app.services.llm_client import call_llm

class BackendAgent:
    def generate_api(self, story, project_name, base_path):
        prompt = f"""
Generate FastAPI backend code.

Story:
Title: {story['title']}
Description: {story.get('description', '')}

Rules:
- Use FastAPI
- JWT if authentication related
- Input validation using Pydantic
- No database connections
- Clean REST endpoints only
"""

        code = call_llm(prompt)

        base = os.path.join(base_path, "backend", "routes")
        os.makedirs(base, exist_ok=True)

        path = os.path.join(base, "api.py")
        with open(path, "w", encoding="utf-8") as f:
            f.write(code)

        return {"status": "OK", "file": path}
