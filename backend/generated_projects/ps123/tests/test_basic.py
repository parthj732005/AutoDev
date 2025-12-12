Below are some minimal pytest tests for a FastAPI login API, adhering to your guidelines. You can use the FastAPI testing capabilities with TestClient to simulate requests without relying on external dependencies.

First, ensure that you have FastAPI and pytest installed. If not, install them using:

```bash
pip install fastapi[all] pytest
```

Now, here is a snippet for a simple FastAPI login API along with the corresponding pytest tests.

### FastAPI Application (main.py)

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    username: str
    password: str

fake_user_db = {"user": "password"}

@app.post("/login")
async def login(user: User):
    if user.username in fake_user_db and user.password == fake_user_db[user.username]:
        return {"msg": "Login successful"}
    raise HTTPException(status_code=400, detail="Invalid credentials")
```

### Pytest Tests (test_main.py)

```python
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_successful_login():
    response = client.post("/login", json={"username": "user", "password": "password"})
    assert response.status_code == 200
    assert response.json() == {"msg": "Login successful"}

def test_unsuccessful_login_invalid_username():
    response