import os

class FrontendAgent:
    def generate_ui(self, work_item: dict, project_name: str):
        base = f"../generated_projects/{project_name}/backend/routes"
        os.makedirs(base, exist_ok=True)

        title = work_item.get("title", "Generated UI")

        code = f"""
export default function GeneratedComponent() {{
  return (
    <div style={{ padding: "20px" }}>
      <h1>{title}</h1>
    </div>
  );
}}
"""

        path = f"{base}/Generated.jsx"
        with open(path, "w", encoding="utf-8") as f:
            f.write(code)

        return f"Frontend created at {path}"
