from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from app.database import get_session
from app.schemas import PatchDetail, PatchListResponse
from app.services.catalog import get_patch_detail, get_patch_list


router = APIRouter(prefix="/patches", tags=["patches"])


@router.get("", response_model=PatchListResponse)
def list_patches(
    platform: str | None = None,
    q: str | None = None,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=12, ge=1, le=50),
    session: Session = Depends(get_session),
) -> PatchListResponse:
    return get_patch_list(session, platform=platform, q=q, page=page, page_size=page_size)


@router.get("/{version}", response_model=PatchDetail)
def patch_detail(version: str, session: Session = Depends(get_session)) -> PatchDetail:
    patch = get_patch_detail(session, version)
    if patch is None:
        raise HTTPException(status_code=404, detail="Patch not found")
    return patch

