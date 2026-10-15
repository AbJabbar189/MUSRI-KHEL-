import os
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "مصری خیل قومی اتحاد فاؤنڈیشن"
    PROJECT_NAME_EN: str = "Misri Khel Qaumi Ittehad"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "super-secret-dev-key-change-in-prod-misri-khel-2026")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day
    BASE_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    DEFAULT_DB_PATH: str = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")), "misri_khel.db").replace("\\", "/")
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{DEFAULT_DB_PATH}")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() in ("true", "1")
    CORS_ORIGINS: List[str] = ["*"]
    BASE_URL: str = os.getenv("BASE_URL", "http://127.0.0.1:8000")
    
    # Community & Organization Info
    ORGANIZATION_MOTTO: str = "اتحاد • خدمت • عزت • ترقی"
    ORGANIZATION_MOTTO_EN: str = "Unity • Service • Honor • Progress"
    PRIMARY_REGIONS: List[str] = ["Karachi", "Shangla", "Torghar", "Buner", "Swat", "Islamabad", "Rawalpindi"]
    
    # Media & Upload paths
    STATIC_DIR: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
    CARDS_DIR: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "cards")
    QR_DIR: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "qr")
    UPLOADS_DIR: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "uploads")
    
    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()

# Ensure directories exist
os.makedirs(settings.CARDS_DIR, exist_ok=True)
os.makedirs(settings.QR_DIR, exist_ok=True)
os.makedirs(settings.UPLOADS_DIR, exist_ok=True)
