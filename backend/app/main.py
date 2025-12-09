from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, projects

app = FastAPI(title="AutoDev Backend")

# CORS so frontend (Vite on 5173) can talk to backend (8000)
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],      # allow GET, POST, OPTIONS, etc
    allow_headers=["*"],      # allow all headers
)
from app.routes import logs

# Routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(projects.router, prefix="/projects", tags=["Projects"])

app.include_router(logs.router, prefix="/logs", tags=["Logs"])
