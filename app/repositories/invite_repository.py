from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.invite import Invite


class InviteRepository:
    async def create(self, db: AsyncSession, invite: Invite):
        db.add(invite)
        await db.commit()
        await db.refresh(invite)
        return invite

    async def get_by_code(self, db: AsyncSession, code: str):
        result = await db.execute(select(Invite).where(Invite.code == code))
        return result.scalar_one_or_none()

    async def get_by_email(self, db: AsyncSession, email: str):
        result = await db.execute(select(Invite).where(Invite.email == email))
        return result.scalar_one_or_none()

    async def list_by_school(self, db: AsyncSession, school_id: str):
        result = await db.execute(select(Invite).where(Invite.school_id == school_id))
        return result.scalars().all()
