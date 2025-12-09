from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import auth, projects, logs, files, download

app = FastAPI(title="AutoDev Backend")

# CORS so frontend (Vite on 5173) can talk to backend (8000)
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # ✅ use defined origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router, prefix="/auth")
app.include_router(projects.router, prefix="/projects")
app.include_router(logs.router, prefix="/logs")
app.include_router(files.router, prefix="/files")
app.include_router(download.router, prefix="/download")
