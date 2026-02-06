"""Application configuration"""
from typing import List
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, PostgresDsn, validator


class Settings(BaseSettings):
    """Application settings"""

    # Project metadata
    PROJECT_NAME: str = "Elenchos"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str | List[str]) -> List[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Database
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "elenchos"
    POSTGRES_PASSWORD: str = "elenchos"
    POSTGRES_DB: str = "elenchos"
    POSTGRES_PORT: str = "5432"
    DATABASE_URL: PostgresDsn | None = None

    @validator("DATABASE_URL", pre=True)
    def assemble_db_connection(cls, v: str | None, values: dict) -> str:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            username=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            port=int(values.get("POSTGRES_PORT", 5432)),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    # ChromaDB
    CHROMA_HOST: str = "localhost"
    CHROMA_PORT: int = 8000
    CHROMA_COLLECTION_NAME: str = "elenchos_rag"

    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    # JWT
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # Rate Limiting
    RATE_LIMIT_LOGIN_ATTEMPTS: int = 5
    RATE_LIMIT_WINDOW_SECONDS: int = 300  # 5 minutes

    # AI Models
    ANTHROPIC_API_KEY: str = ""
    GOOGLE_API_KEY: str = ""
    AI_TIMEOUT_SECONDS: int = 30

    # Docker Sandbox
    DOCKER_TIMEOUT_SECONDS: int = 1
    DOCKER_MEMORY_LIMIT: str = "256m"
    DOCKER_CPU_LIMIT: float = 1.0

    # BKT Parameters
    BKT_P_L0: float = 0.1  # Initial knowledge probability
    BKT_P_T: float = 0.3   # Learning probability
    BKT_P_S: float = 0.1   # Slip probability
    BKT_P_G: float = 0.2   # Guess probability
    BKT_MASTERY_THRESHOLD: float = 0.7

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
