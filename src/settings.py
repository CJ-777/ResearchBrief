from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str
    openrouter_api_key: str
    langsmith_api_key: str = ""
    langsmith_tracing: bool = True
    langsmith_project: str = "research-briefs"
    langsmith_otel_enabled: bool = True
    serp_api_key: str

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
