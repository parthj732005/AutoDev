import os
class BackendAgent:
    def generate_api(self, work_item: dict, project_name: str):
        """
        Rule-based backend generator.

        - Creates folder: generated_projects/{project_name}/backend/routes
        - If title contains 'login' -> generates login.py
        - Otherwise -> generates generic.py
        """
        base = f"../generated_projects/{project_name}/backend/routes"
        os.makedirs(base, exist_ok=True)

        title = work_item.get("title", "")
        title_lower = title.lower()

        if "login" in title_lower:
            filename = "login.py"
            code = self._login_api()
        else:
            filename = "generic.py"
            code = self._generic_api(title)

        path = os.path.join(base, filename)

        with open(path, "w", encoding="utf-8") as f:
            f.write(code)

        return f"Created {path}"

    # ---------------------------
    # RULE: AUTH / LOGIN TEMPLATE
    # ---------------------------
    def _login_api(self) -> str:
        """
        Very simple login API (no hashing to avoid extra deps).
        """
        return '''from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr

router = APIRouter()

# Dummy in-memory user DB
fake_users_db = {
    "user@example.com": {
        "email": "user@example.com",
        "password": "secret_password",
    }
}

class UserLogin(BaseModel):
    email: EmailStr
    password: str


def authenticate_user(email: str, password: str):
    user = fake_users_db.get(email)
    if not user:
        return None
    if password != user["password"]:
        return None
    return user


@router.post("/login")
def login(user: UserLogin):
    authenticated_user = authenticate_user(user.email, user.password)
    if not authenticated_user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return {"message": "Login successful"}
'''

    # ---------------------------
    # RULE: GENERIC ENDPOINT
    # ---------------------------
    def _generic_api(self, title: str) -> str:
        """
        Fallback generic endpoint when we don't match a more specific rule.
        """
        safe_name = (title or "endpoint").strip().lower().replace(" ", "_")
        if not safe_name:
            safe_name = "endpoint"

        return f'''from fastapi import APIRouter

router = APIRouter()

@router.get("/{safe_name}")
def handler():
    return {{"message": "{title} endpoint"}}
'''
