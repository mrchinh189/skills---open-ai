from __future__ import annotations

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "sqlite:///./vbiz.db"
    secret_key: str = "dev-secret-change-me-32-characters-please"
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    skills_dir: str = "../skills/.business-vn"
    env: str = "dev"

    @property
    def skills_path(self) -> Path:
        return (Path(__file__).resolve().parents[1] / self.skills_dir).resolve()


settings = Settings()
