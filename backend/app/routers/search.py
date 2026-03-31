from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from app.database import get_session
from app.schemas import SearchResponse
from app.services.search import query_search_index


router = APIRouter(prefix="/search", tags=["search"])


@router.get("", response_model=SearchResponse)
def search(
    q: str = Query(default=""),
    platform: str | None = None,
    limit: int = Query(default=10, ge=1, le=25),
    session: Session = Depends(get_session),
) -> SearchResponse:
    return query_search_index(session, q, platform, limit)

