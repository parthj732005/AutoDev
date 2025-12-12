Certainly! Below is a minimal setup for testing a FastAPI login API using pytest. This example includes a simple FastAPI app with a login endpoint and corresponding tests.

### FastAPI Application (app.py)

```python
from fastapi import FastAPI, Depends, HTTPException

app = FastAPI()

fake_users_db = {
    "user1": {"username": "user1", "password": "password1"},
}

@app.post("/login")
async def login(username: str, password: str):
    user = fake_users_db.get(username)
    if not user or user['password'] != password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"message": "Login successful"}
```

### Pytest Tests (test_app.py)

```python
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_login_success():
    response = client.post("/login", json={"username": "user1", "password": "password1"})
    assert response.status_code == 200
    assert response.json() == {"message": "Login successful"}

def test_login_failure_wrong_username():
    response = client.post("/login", json={"username": "wrong_user", "password": "password1"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Incorrect username or password"}

def test_login_failure_wrong_password():
    response = client.post("/login