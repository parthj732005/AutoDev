To create minimal pytest tests for a FastAPI login API, we need to establish a basic FastAPI application with a login endpoint and then write the tests using pytest. Below is the code for the FastAPI application and the corresponding pytest tests.

### FastAPI Application (`app.py`)

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/login")
async def login(request: LoginRequest):
    if request.username == "testuser" and request.password == "testpass":
        return {"message": "Login successful"}
    raise HTTPException(status_code=401, detail="Invalid credentials")
```

### Pytest Tests (`test_app.py`)

```python
import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_login_success():
    response = client.post("/login", json={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200
    assert response.json() == {"message": "Login successful"}

def test_login_failure():
    response = client.post("/login", json={"username": "wronguser", "password": "wrongpass"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}
```

### Explanation

1. **FastAPI