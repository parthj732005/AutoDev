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
- Use Pydantic models for request and response
- If authentication or login related, create real API endpoints
- Assume a database exists and endpoints are real
- If the frontend is expected to call this API, do NOT mock data
- Assume real requests will come from a frontend
- Do NOT implement database connection logic
- Keep implementation simple and runnable
"""

        result = call_llm(prompt, max_tokens=800)["content"]

        base = os.path.join(base_path, "backend")
        os.makedirs(base, exist_ok=True)

        path = os.path.join(base, "api.py")
        with open(path, "w", encoding="utf-8") as f:
            f.write(result)

        return {"status": "OK", "file": path}
