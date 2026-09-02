from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    APP_NAME: str = "Ezitech EEF - Auto Evaluation Platform"
    ENV: str = "development"
    DEBUG: bool = True

    DATABASE_URL: str = "postgresql://eef_user:eef_pass@localhost:5432/eef_db"
    REDIS_URL: str = "redis://localhost:6379/0"

    SANDBOX_TIMEOUT_SECONDS: int = 300
    SANDBOX_WORKDIR: str = "/tmp/eef_sandbox"

    LLM_API_KEY: str = ""
    LLM_MODEL: str = "claude-sonnet-4-6"

    SECRET_KEY: str = "change_this_in_production"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
