from fastapi import APIRouter, HTTPException
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
