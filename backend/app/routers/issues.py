from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from app.database import get_session
from app.schemas import IssueDetail, IssueListResponse
from app.services.catalog import get_issue_detail, get_issue_list


router = APIRouter(prefix="/issues", tags=["issues"])


@router.get("", response_model=IssueListResponse)
def list_issues(
    platform: str | None = None,
    status: str | None = None,
    category: str | None = None,
    q: str | None = None,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=12, ge=1, le=50),
    session: Session = Depends(get_session),
) -> IssueListResponse:
    return get_issue_list(
        session,
        platform=platform,
        status=status,
        category=category,
        q=q,
        page=page,
        page_size=page_size,
    )


@router.get("/{slug}", response_model=IssueDetail)
def issue_detail(slug: str, session: Session = Depends(get_session)) -> IssueDetail:
    issue = get_issue_detail(session, slug)
    if issue is None:
        raise HTTPException(status_code=404, detail="Issue not found")
    return issue
