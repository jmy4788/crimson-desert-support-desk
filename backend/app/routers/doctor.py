from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database import get_session
from app.schemas import DoctorQueryInput, DoctorQueryResponse
from app.services.doctor import build_doctor_response


router = APIRouter(prefix="/settings-doctor", tags=["settings-doctor"])


@router.post("/query", response_model=DoctorQueryResponse)
def query_doctor(payload: DoctorQueryInput, session: Session = Depends(get_session)) -> DoctorQueryResponse:
    return build_doctor_response(session, payload)

