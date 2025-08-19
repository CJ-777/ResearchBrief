from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str
    anthropic_api_key: str = ""
    langsmith_api_key: str = ""
    langsmith_tracing: bool = True
    langsmith_project: str = "research-briefs"
    serp_api_key: str
    port: int = 8000

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
