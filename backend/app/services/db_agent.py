import os

class DatabaseAgent:
    def generate_schema(self, project_name: str, entity="users"):
        base = f"../generated_projects/{project_name}/frontend"

        os.makedirs(base, exist_ok=True)

        code = f"""
CREATE TABLE {entity} (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE,
    password TEXT
);
"""
        path = f"{base}/{entity}.sql"
        with open(path, "w") as f:
            f.write(code)

        return f"DB schema created: {path}"
