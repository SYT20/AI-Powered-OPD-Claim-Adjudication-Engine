from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./plum_opd.db"
    GEMINI_API_KEY: str
    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE: int = 10485760
    
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Plum OPD Claim Adjudication"
    VERSION: str = "1.0.0"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
