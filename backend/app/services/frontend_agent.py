import os
from app.services.llm_client import call_llm

class FrontendAgent:
    def generate_ui(self, story, project_name, base_path):
        prompt = f"""
Generate a React JSX component.

Story:
{story['title']}
{story.get('description', '')}

Rules:
- Functional React component
- Tailwind CSS classes only
- No external libraries
- No npm installs assumed
"""

        code = call_llm(prompt)

        base = os.path.join(base_path, "frontend")
        os.makedirs(base, exist_ok=True)

        path = os.path.join(base, "Generated.jsx")
        with open(path, "w", encoding="utf-8") as f:
            f.write(code)

        return {"status": "OK", "file": path}
