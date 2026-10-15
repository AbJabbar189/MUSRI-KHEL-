import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.database.session import Base, engine
from app.api.api_router import api_router
import app.models  # Ensure all models are registered

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Misri Khel Qaumi Ittehad - Digital Community Platform & Secretariat Management System",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health endpoint (must be defined before catch-all static mounts)
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "organization": settings.PROJECT_NAME,
        "organization_en": settings.PROJECT_NAME_EN,
        "motto": settings.ORGANIZATION_MOTTO
    }

# API Routes
app.include_router(api_router)

# Mount backend static files (cards, qr codes, logos, downloads)
app.mount("/static", StaticFiles(directory=settings.STATIC_DIR), name="static")

# Mount web files (supports both root directory and legacy frontend directory)
root_workspace_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".."))
frontend_dir = os.path.join(root_workspace_dir, "frontend")

if os.path.exists(frontend_dir):
    app.mount("/frontend", StaticFiles(directory=frontend_dir, html=True), name="frontend")
    public_dir = os.path.join(frontend_dir, "public")
    if os.path.exists(public_dir):
        app.mount("/public", StaticFiles(directory=public_dir, html=True), name="public_explicit")
        app.mount("/", StaticFiles(directory=public_dir, html=True), name="public")
else:
    # Files are placed directly in project root
    app.mount("/", StaticFiles(directory=root_workspace_dir, html=True), name="root_site")
