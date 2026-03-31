from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request

from app.schemas import SeedRequest, SeedResponse
from app.services.seed import seed_database


router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/seed", response_model=SeedResponse)
def admin_seed(request: Request, payload: SeedRequest | None = None) -> SeedResponse:
    settings = request.app.state.settings
    if settings.is_production:
        raise HTTPException(status_code=403, detail="Seed endpoint is disabled in production")

    seeded_counts = seed_database(
        request.app.state.engine,
        settings.seed_path,
        reset=payload.reset if payload is not None else False,
    )
    return SeedResponse(seeded_counts=seeded_counts)

