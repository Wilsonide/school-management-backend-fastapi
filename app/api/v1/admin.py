from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import RequireSuperAdmin
from app.db.database import get_db
from app.services.admin_service import AdminService

router = APIRouter(
    prefix="/admin",
    tags=["Super Admin"],
)

service = AdminService()


# =====================================
# DASHBOARD STATS
# =====================================
@router.post("/create-school-admin")
async def create_school_admin(
    payload: dict,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: RequireSuperAdmin,
):
    user = await service.create_school_admin(db, payload)

    if not user:
        raise HTTPException(status_code=400, detail="Failed to create admin")

    return {
        "message": "School admin created",
        "user": user,
    }


@router.delete("/admins/{user_id}")
async def delete_admin(
    user_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: RequireSuperAdmin,
):
    result = await service.delete_admin(db, user_id)

    if not result:
        raise HTTPException(status_code=404, detail="Admin not found")

    return {
        "message": "Admin deleted",
    }


@router.get("/stats")
async def get_dashboard_stats(
    db: Annotated[AsyncSession, Depends(get_db)],
    _: RequireSuperAdmin,
):
    return await service.get_dashboard_stats(db)


@router.get("/admins")
async def get_admins(
    db: Annotated[AsyncSession, Depends(get_db)],
    _: RequireSuperAdmin,
):
    admins = await service.get_admins(db)

    return {
        "message": "Admins fetched successfully",
        "admins": admins,
    }


# =====================================
# ASSIGN SCHOOL ADMIN
# =====================================


@router.post("/users/{user_id}/assign-school-admin/{school_id}")
async def assign_school_admin(
    user_id: str,
    school_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: RequireSuperAdmin,
):
    user = await service.assign_school_admin(
        db,
        user_id,
        school_id,
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


# =====================================
# REVOKE SCHOOL ADMIN
# =====================================


@router.post("/users/{user_id}/revoke-school-admin")
async def revoke_school_admin(
    user_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: RequireSuperAdmin,
):
    user = await service.revoke_school_admin(
        db,
        user_id,
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return {
        "message": "School admin revoked",
        "user": user,
    }
