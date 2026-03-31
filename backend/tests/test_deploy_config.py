from __future__ import annotations

from app.config import Settings
from app.database import normalize_database_url


def test_settings_parses_comma_separated_cors_origins() -> None:
    settings = Settings(
        cors_origins="https://support.example.com, https://www.support.example.com",
    )

    assert settings.cors_origins == [
        "https://support.example.com",
        "https://www.support.example.com",
    ]


def test_normalize_database_url_for_render_postgres() -> None:
    assert normalize_database_url("postgres://user:pass@host:5432/db") == "postgresql+psycopg://user:pass@host:5432/db"
    assert normalize_database_url("postgresql://user:pass@host:5432/db") == "postgresql+psycopg://user:pass@host:5432/db"
