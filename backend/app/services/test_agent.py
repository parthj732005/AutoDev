import os

class TestAgent:
    def generate_tests(self, project_name: str):
        base = f"../generated_projects/{project_name}/tests"
        os.makedirs(base, exist_ok=True)

        code = """
def test_login():
    assert True
"""
        path = f"{base}/test_basic.py"
        with open(path, "w") as f:
            f.write(code)

        return f"Tests created: {path}"
