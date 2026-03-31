from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from sqlmodel import Session

from app.database import get_session
from app.schemas import HealthResponse
from app.services.catalog import get_health


router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
def healthcheck(request: Request, session: Session = Depends(get_session)) -> HealthResponse:
    return get_health(session, request.app.state.settings.app_env)

