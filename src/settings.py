from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str
    openrouter_api_key: str
    langsmith_api_key: str = ""  # optional; default empty string
    langsmith_tracing: bool = True
    langsmith_project: str = "research-briefs"
    langsmith_otel_enabled: bool = True
    serp_api_key: str  # required

    class Config:
        env_file = ".env"  # load environment variables from .env
        case_sensitive = False  # makes env var keys case-insensitive


settings = Settings()
