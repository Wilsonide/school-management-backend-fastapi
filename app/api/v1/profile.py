from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import CurrentUser
from app.db.database import get_db

from app.services.profile_service import ProfileService



router = APIRouter(tags=["Profile"], prefix="/profile")

profile_service = ProfileService()


@router.get("/me")
async def get_my_profile(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: CurrentUser,
):
    profile = await profile_service.get_by_user_id(
        db=db,
        user=current_user,
    )

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Profile not found",
        )

    return {
        "profile": profile,
    }


@router.patch("/me")
async def update_my_profile(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: CurrentUser,

    payload: dict,  # we validate inside service using schemas
):
    updated = await profile_service.update_profile(
        db=db,
        user=current_user,
        payload=payload,
    )

    return {
        "message": "Profile updated",
        "profile": updated,
    }

@router.post("/create")
async def create_profile(
    payload: dict,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: CurrentUser,
):
    """
    Creates profile after signup/login onboarding step
    """

    if current_user.profile_completed:
        raise HTTPException(
            status_code=400,
            detail="Profile already exists",
        )

    profile = await profile_service.create_profile(
        db=db,
        user=current_user,
        payload=payload,
    )

    return {
        "message": "Profile created successfully",
        "profile": profile,
    }