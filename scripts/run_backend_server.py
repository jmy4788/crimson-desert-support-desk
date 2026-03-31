from __future__ import annotations

import os
from pathlib import Path
import sys

import uvicorn


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from support_desk_asgi import app  # noqa: E402


if __name__ == "__main__":
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", os.getenv("SUPPORT_DESK_PORT", "8017")))
    uvicorn.run(app, host=host, port=port)
