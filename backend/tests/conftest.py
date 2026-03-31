from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app


REPO_ROOT = Path(__file__).resolve().parents[2]
SEED_PATH = REPO_ROOT / "data" / "seeds" / "sample_data.json"


@pytest.fixture
def client(tmp_path: Path) -> TestClient:
    database_path = tmp_path / "test_support_desk.db"
    settings = Settings(
        app_env="test",
        database_url=f"sqlite:///{database_path.as_posix()}",
        seed_path=SEED_PATH,
        auto_seed_on_start=True,
    )
    app = create_app(settings)
    with TestClient(app) as test_client:
        yield test_client

