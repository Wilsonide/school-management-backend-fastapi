from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.services.invite_service import InviteService

router = APIRouter(prefix="/invites", tags=["Invites"])

invite_service = InviteService()


# =====================================================
# GET ALL INVITES (SCHOOL ADMIN)
# =====================================================
@router.get("/{school_id}")
async def get_school_invites(
    school_id: str, db: Annotated[AsyncSession, Depends(get_db)]
):
    invites = await invite_service.repo.list_by_school(db, school_id)

    return invites


# =====================================================
# CREATE INVITE MANUALLY (OPTIONAL ADMIN TOOL)
# =====================================================
@router.post("/")
async def create_invite(payload: dict, db: Annotated[AsyncSession, Depends(get_db)]):
    invite = await invite_service.create_auto_invite(
        db,
        payload["school_id"],
        payload["email"],
        payload["role"],
    )

    return {"message": "Invite created", "invite": invite}


# =====================================================
# VALIDATE INVITE (DEBUG / FRONTEND CHECK)
# =====================================================
@router.get("/validate/{code}")
async def validate_invite(code: str, db: Annotated[AsyncSession, Depends(get_db)]):
    invite = await invite_service.get_by_code(db, code)

    if not invite:
        raise HTTPException(status_code=404, detail="Invite not found")

    return {
        "valid": not invite.is_used,
        "email": invite.email,
        "role": invite.role,
        "school_id": invite.school_id,
    }
