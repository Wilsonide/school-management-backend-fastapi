from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import RequireSuperAdmin
from app.db.database import get_db

from app.services.school_service import SchoolService

router = APIRouter(
    prefix="/schools",
    tags=["Schools"],
)

service = SchoolService()

# =====================================================
# GET ALL SCHOOLS
# =====================================================
@router.get("/")
async def get_schools(
    db: Annotated[
        AsyncSession,
        Depends(get_db),
    ],
    _: RequireSuperAdmin,
):
    schools = await service.get_schools(db)

    return {
        "schools": schools,
    }


# =====================================================
# CREATE SCHOOL
# =====================================================
@router.post("/")
async def create_school(
    payload: dict,
    db: Annotated[
        AsyncSession,
        Depends(get_db),
    ],
    _: RequireSuperAdmin,
):
    school = await service.create_school(
        db,
        payload,
    )

    return {
        "message": "School created successfully",
        "school": school,
    }


# =====================================================
# DELETE SCHOOL
# =====================================================
@router.delete("/{school_id}")
async def delete_school(
    school_id: str,
    db: Annotated[
        AsyncSession,
        Depends(get_db),
    ],
    _: RequireSuperAdmin,
):
    deleted = await service.delete_school(
        db,
        school_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="School not found",
        )

    return {
        "message": "School deleted successfully",
    }


# =====================================================
# ASSIGN SCHOOL ADMIN
# =====================================================
@router.post("/{school_id}/assign-admin/{user_id}")
async def assign_admin(
    school_id: str,
    user_id: str,
    db: Annotated[
        AsyncSession,
        Depends(get_db),
    ],
    _: RequireSuperAdmin,
):
    user = await service.assign_admin(
        db,
        school_id,
        user_id,
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User or School not found",
        )

    return {
        "message": "School admin assigned successfully",
        "user": user,
    }