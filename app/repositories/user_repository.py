from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.school import School
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
    async def get_by_username(self, db: AsyncSession, user_name: str):
        result = await db.execute(
            select(User).where(User.username == user_name)
        )
        return result.scalar_one_or_none()
    async def get_school_by_slug(
        self,
        db: AsyncSession,
        slug: str,
    ):
        result = await db.execute(
            select(School).where(School.slug == slug)
        )

        return result.scalar_one_or_none()

    async def get_user_by_username_and_school(
        self,
        db: AsyncSession,
        username: str,
        school_id: str,
    ):
        result = await db.execute(
            select(User).where(
                User.username == username,
                User.school_id == school_id,
            )
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

    async def get_school_by_slug(
    self,
    db,
    slug: str,
):
        result = await db.execute(
            select(School).where(
                School.slug == slug
            )
        )

        return result.scalar_one_or_none()
    async def get_by_school_slug_and_username(
    self,
    db,
    school_slug: str,
    username: str,
):
        result = await db.execute(
            select(User)
            .join(
                School,
                User.school_id == School.id,
            )
            .where(
                School.slug == school_slug,
                User.username == username,
            )
        )

        return result.scalar_one_or_none()

user_repo = UserRepository()