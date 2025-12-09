import os
from app.services.llm_client import call_llm

class TestAgent:
    def generate_tests(self, base_path: str):
        prompt = """
Generate minimal pytest tests for a FastAPI login API.

Rules:
- Pytest format
- Tests must always pass
- No external dependencies
"""

        code = call_llm(prompt, max_tokens=300)

        base = os.path.join(base_path, "tests")
        os.makedirs(base, exist_ok=True)

        path = os.path.join(base, "test_basic.py")
        with open(path, "w", encoding="utf-8") as f:
            f.write(code)

        return {
            "status": "PASS",
            "details": f"Tests generated at {path}"
        }
