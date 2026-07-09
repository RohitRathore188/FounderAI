import os
from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Fix TLS certificate issues on Windows
os.environ.pop("CURL_CA_BUNDLE", None)
os.environ.pop("SSL_CERT_FILE", None)


class Settings(BaseSettings):
    # Project Settings
    PROJECT_NAME: str = "FounderAI"
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"

    # Gemini API Key
    GEMINI_API_KEY: str = Field(default="", env="GEMINI_API_KEY")
    TAVILY_API_KEY: str = Field(default="", env="TAVILY_API_KEY")

    # Allowed Frontend Origins
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://founder-ai-one.vercel.app",
    ]

    model_config = SettingsConfigDict(
        env_file=os.path.join(
            os.path.dirname(
                os.path.dirname(
                    os.path.dirname(__file__)
                )
            ),
            ".env",
        ),
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()