from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import auth, projects, logs, files, download
from app.db.init_db import init_db

# ✅ FIRST create the app
app = FastAPI(title="AutoDev Backend")


@app.get("/health")
def health():
    return {"status": "ok"}



# ✅ THEN startup event
@app.on_event("startup")
def startup():
    init_db()

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # fine for development
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Routers
app.include_router(auth.router, prefix="/auth")
app.include_router(projects.router, prefix="/projects")
app.include_router(logs.router, prefix="/logs")
app.include_router(files.router, prefix="/files")
app.include_router(download.router, prefix="/download")
