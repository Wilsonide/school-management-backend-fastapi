# app/api/v1/endpoints/academic.py

from fastapi import APIRouter

from app.core.deps import (
    CurrentUser,
    DBSession,
)
from app.schemas.academic_schema import ActiveAcademicResponse
from app.services.academic_services import academic_service

router = APIRouter(
    prefix="/academic",
    tags=["Academic"],
)


@router.get(
    "/active",
    response_model=ActiveAcademicResponse,
)
async def get_active_academic_period(
    db: DBSession,
    user: CurrentUser,
):
    return await academic_service.get_active_period(
        db,
        user.school_id,
    )
