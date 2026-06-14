from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class UserRepository:

    async def create(self, db: AsyncSession, user: User):
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    # =====================================
    # GET BY EMAIL
    # =====================================
    async def get_by_email(self, db: AsyncSession, email: str):
        result = await db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()
    

    
    async def save_access_token(self, db: AsyncSession, user: User, access_token: str):
        user.access_token = access_token
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    # =====================================
    # GET BY ID
    # =====================================
    async def get_by_id(self, db: AsyncSession, user_id: str):
        result = await db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    # =====================================
    # GET ALL USERS
    # =====================================
    async def get_all(self, db: AsyncSession):
        result = await db.execute(
            select(User).order_by(User.created_at.desc())
        )
        return result.scalars().all()

    # =====================================
    # DELETE USER
    # =====================================
    async def delete(self, db: AsyncSession, user: User):
        await db.delete(user)
        await db.commit()