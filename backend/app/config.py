from __future__ import annotations

import json
from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DB_PATH = REPO_ROOT / "data" / "runtime" / "support_desk.db"
DEFAULT_SEED_PATH = REPO_ROOT / "data" / "seeds" / "sample_data.json"


class Settings(BaseSettings):
    app_name: str = "Crimson Desert Support Desk API"
    app_env: str = "dev"
    api_prefix: str = "/api"
    database_url: str = f"sqlite:///{DEFAULT_DB_PATH.as_posix()}"
    seed_path: Path = DEFAULT_SEED_PATH
    auto_seed_on_start: bool = True
    cors_origins: list[str] = [
        "http://localhost:4173",
        "http://127.0.0.1:4173",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

    model_config = SettingsConfigDict(
        env_prefix="SUPPORT_DESK_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: object) -> object:
        if isinstance(value, str):
            text = value.strip()
            if not text:
                return []
            if text.startswith("["):
                return json.loads(text)
            return [item.strip() for item in text.split(",") if item.strip()]
        return value

    @property
    def is_production(self) -> bool:
        return self.app_env.lower() == "prod"
