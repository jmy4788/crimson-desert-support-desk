from __future__ import annotations

from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "backend"))

from app.config import Settings
from app.database import create_db_engine, init_database
from app.services.seed import seed_database


if __name__ == "__main__":
    settings = Settings(
        database_url=f"sqlite:///{(REPO_ROOT / 'data' / 'runtime' / 'support_desk.db').as_posix()}",
        seed_path=REPO_ROOT / "data" / "seeds" / "sample_data.json",
    )
    engine = create_db_engine(settings.database_url)
    init_database(engine)
    counts = seed_database(engine, settings.seed_path, reset=True)
    print("Seed complete:", counts)
