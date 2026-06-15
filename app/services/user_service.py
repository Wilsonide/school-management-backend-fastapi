from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.services.profile_service import ProfileService


class UserService:

    def __init__(self):
        self.repo = UserRepository()
        self.profile_service = ProfileService()

    # =====================================
    # CREATE USER + PROFILE
    # =====================================
    async def create_user_with_profile(
        self,
        db: AsyncSession,
        email: str,
        password: str,
        role,
        school_id: str,
    ):
        user = User(
            email=email,
            password=password,
            role=role,
            school_id=school_id,
            profile_completed=False,
        )

        user = await self.repo.create(db, user)

        await self.profile_service.create_profile(db, user)

        return user
    async def get_school_by_slug(
    self,
    db,
    slug: str,
):
        return await self.repo.get_school_by_slug(
            db,
            slug,
        )
    # =====================================
    # GET USER BY EMAIL
    # =====================================
    async def get_by_email(self, db, email: str):
        return await self.repo.get_by_email(db, email)

    # =====================================
    # GET USER BY ID
    # =====================================
    async def get_by_id(self, db, user_id: str):
        return await self.repo.get_by_id(db, user_id)
    
    async def get_by_username(self, db, username: str):
        return await self.repo.get_by_username(db, username)

    # =====================================
    # GET ALL USERS
    # =====================================
    async def get_all_users(self, db):
        return await self.repo.get_all(db)
    
    async def get_by_school_slug_and_username(
    self,
    db,
    school_slug: str,
    username: str,
):
        return await self.repo.get_by_school_slug_and_username(
            db,
            school_slug,
            username,
        )

    # =====================================
    # DELETE USER
    # =====================================
    async def delete_user(self, db, user_id: str):
        user = await self.repo.get_by_id(db, user_id)

        if not user:
            return None

        await self.repo.delete(db, user)

        return True


userservice = UserService()