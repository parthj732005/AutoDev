import os
from app.services.llm_client import LLMClient

class LLMBackendAgent:
    def __init__(self):
        self.llm = LLMClient()

    def generate_api(self, work_item: dict, project_name: str, base_path: str):
        base = os.path.join(base_path, "backend", "routes")
        os.makedirs(base, exist_ok=True)

        prompt = f"""
Generate a FastAPI route for this requirement:

Title: {work_item['title']}
Description: {work_item.get('description', '')}

Return ONLY valid Python code.
"""

        code = self.llm.generate_code(prompt)
        filename = "llm_generated.py"
        path = f"{base}/{filename}"

        with open(path, "w", encoding="utf-8") as f:
            f.write(code)

        return f"LLM Backend API created: {path}"
