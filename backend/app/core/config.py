"""
Application configuration using Pydantic Settings
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Database
    mongodb_uri: str = "mongodb://localhost:27017/fitai"

    # OpenAI
    openai_api_key: str = ""

    # JWT
    jwt_secret: str = ""
    jwt_algorithm: str = "HS256"

    # Environment
    environment: str = "development"

    # CORS
    frontend_api_base_url: str = "http://localhost:5173"
    ios_api_base_url: str = "http://localhost:8000"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()

