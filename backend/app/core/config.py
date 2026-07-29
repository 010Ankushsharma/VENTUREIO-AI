"""
Application configuration via environment variables.
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    APP_NAME: str = "VentureIQ AI"
    APP_ENV: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str = "change-me-in-production"

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://ventureiq:password@db:5432/ventureiq"
    REDIS_URL: str = "redis://redis:6379/0"

    # AI
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    LLM_PROVIDER: str = "openai"
    LLM_MODEL: str = "gpt-4o"

    # Vector DB
    QDRANT_HOST: str = "qdrant"
    QDRANT_PORT: int = 6333
    QDRANT_COLLECTION: str = "ventureiq_docs"

    # Auth
    JWT_SECRET: str = "jwt-secret-change-me"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 1440

    # Storage
    AWS_S3_BUCKET: str = "ventureiq-documents"
    AWS_REGION: str = "us-east-1"

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
