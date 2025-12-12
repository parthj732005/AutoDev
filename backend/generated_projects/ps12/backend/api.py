Here's a simple FastAPI backend implementation for user authentication using email and password. This implementation includes Pydantic models for request validation and response formatting, as well as the necessary API endpoints for registration and login.

```python
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import List
from passlib.context import CryptContext

app = FastAPI()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Fake user storage (mock replacement for a database)
fake_users_db = {}

# Pydantic models
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    email: EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str

# Utility functions
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def user_exists(email: str) -> bool:
    return email in fake_users_db

def create_user(user: UserCreate) -> UserResponse:
    fake_users_db[user.email] = get_password_hash(user.password)
    return UserResponse(email=user.email)

def authenticate_user(email: str, password: str) -> UserResponse:
    if not user_exists(email) or not verify_password(password, fake_users_db[email]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return UserResponse(email=email)

# API endpoints
@app.post("/register", response_model=UserResponse)
async def register(user: UserCreate):
    if user_exists(user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(user)

@app.post("/login", response_model=Token)
async def login(user: UserCreate):
    user_data = authenticate_user(user.email, user.password)
    # Here we would generate a real access token
    # For demo purposes, we're just returning a placeholder
    access_token = f"fake_token_for_{user_data.email}"
    return {"access_token": access_token, "token_type": "bearer"}

# This is where you can add further security measures such as token validation, but for
# simplicity, these are not included in this example.

# You can run the application by executing:
# `uvicorn filename:app --reload`
```

### Brief Explanation

1. **FastAPI & Pydantic**: We import FastAPI and Pydantic modules to create our web application and handle request/response data neatly.
  
2. **Password Hashing**: We're using `passlib` to hash passwords for secure storage and verification.

3. **Endpoint for User Registration**: 
   - **POST `/register`**: This creates a new user if the email is not already registered.

4. **Endpoint for User Login**:
   - **POST `/login`**: This authenticates the user and returns a fake access token. In a real-world scenario, you would generate a JWT or similar secure token.

5. **User Storage**: The `fake_users_db` dictionary serves as a mock database for user data.

This implementation does not connect to a real database or produce real tokens; however, it sets up the core structure you would build upon for an actual authentication API.