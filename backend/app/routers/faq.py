from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from app.database import get_session
from app.schemas import FAQListResponse
from app.services.catalog import get_faq_list


router = APIRouter(prefix="/faq", tags=["faq"])


@router.get("", response_model=FAQListResponse)
def list_faq(
    q: str | None = None,
    issue_slug: str | None = None,
    patch_version: str | None = None,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=12, ge=1, le=50),
    session: Session = Depends(get_session),
) -> FAQListResponse:
    return get_faq_list(
        session,
        q=q,
        issue_slug=issue_slug,
        patch_version=patch_version,
        page=page,
        page_size=page_size,
    )

