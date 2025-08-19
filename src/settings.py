# src/settings.py
from pydantic import BaseSettings


class Settings(BaseSettings):
    # LLM API keys
    openai_api_key: str
    anthropic_api_key: str

    # LangSmith tracing
    langsmith_api_key: str
    langsmith_tracing: bool = True
    langsmith_project: str = "research-briefs"

    # App configuration
    port: int = 8000

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Singleton instance for easy import
settings = Settings()
