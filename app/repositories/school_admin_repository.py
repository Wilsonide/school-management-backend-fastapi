from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.classes import Class
from app.models.user import User, UserRole


class SchoolAdminRepository:
    # =========================
    # STATS (USERS BASED)
    # =========================
    async def count_students(self, db: AsyncSession, school_id: str):
        result = await db.execute(
            select(func.count(User.id)).where(
                User.school_id == school_id,
                User.role == UserRole.STUDENT,
            ),
        )
        return result.scalar() or 0

    async def count_teachers(self, db: AsyncSession, school_id: str):
        result = await db.execute(
            select(func.count(User.id)).where(
                User.school_id == school_id,
                User.role == UserRole.TEACHER,
            ),
        )
        return result.scalar() or 0

    async def count_classes(self, db: AsyncSession, school_id: str):
        result = await db.execute(
            select(func.count(Class.id)).where(Class.school_id == school_id),
        )
        return result.scalar() or 0

    # =========================
    # LIST STUDENTS (WITH PROFILE JOIN)
    # =========================
    async def get_students(self, db: AsyncSession, school_id: str):
        result = await db.execute(
            select(User).where(
                User.school_id == school_id,
                User.role == UserRole.STUDENT,
            ),
        )
        return result.scalars().all()

    # =========================
    # LIST TEACHERS
    # =========================
    async def get_teachers(self, db: AsyncSession, school_id: str):
        result = await db.execute(
            select(User).where(
                User.school_id == school_id,
                User.role == UserRole.TEACHER,
            ),
        )
        return result.scalars().all()


school_admin_repo = SchoolAdminRepository()
