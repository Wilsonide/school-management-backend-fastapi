from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import CurrentUser
from app.db.database import get_db
from app.services.profile_service import ProfileService

router = APIRouter(
    tags=["Profile"],
    prefix="/profile",
)

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

    return {
        "user": {
            "id": str(current_user.id),
            "first_name": current_user.first_name,
            "last_name": current_user.last_name,
            "email": current_user.email,
            "phone": current_user.phone,
            "role": current_user.role,
            "profile_completed": current_user.profile_completed,
        },
        "profile": profile,
    }


@router.patch("/me")
async def update_my_profile(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: CurrentUser,
    payload: dict,
):
    result = await profile_service.update_profile(
        db=db,
        user=current_user,
        payload=payload,
    )

    return {
        "message": "Profile updated successfully",
        **result,
    }


@router.post("/create")
async def create_profile(
    payload: dict,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: CurrentUser,
):
    existing = await profile_service.get_by_user_id(
        db=db,
        user=current_user,
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Profile already exists",
        )

    try:
        result = await profile_service.create_profile(
            db=db,
            user=current_user,
            payload=payload,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        ) from e
    else:
        return {
            "message": "Profile created successfully",
            **result,
        }
