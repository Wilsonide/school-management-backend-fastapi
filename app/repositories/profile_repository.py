from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.parent import ParentProfile
from app.models.student import StudentProfile
from app.models.teacher import TeacherProfile


class ProfileRepository:
    async def save(self, db, profile):
        db.add(profile)
        await db.commit()
        await db.refresh(profile)
        return profile

    # =====================================================
    # GET STUDENT
    # =====================================================

    async def get_student(self, db, user_id):
        result = await db.execute(
            select(StudentProfile)
            .options(
                selectinload(StudentProfile.user),
            )
            .where(StudentProfile.user_id == user_id),
        )

        return result.scalars().first()

    # =====================================================
    # GET TEACHER
    # =====================================================

    async def get_teacher(self, db, user_id):
        result = await db.execute(
            select(TeacherProfile)
            .options(
                selectinload(TeacherProfile.user),
            )
            .where(TeacherProfile.user_id == user_id)
        )

        return result.scalars().first()

    # =====================================================
    # GET PARENT
    # =====================================================

    async def get_parent(self, db, user_id):
        result = await db.execute(
            select(ParentProfile)
            .options(
                selectinload(ParentProfile.user),
            )
            .where(ParentProfile.user_id == user_id)
        )

        return result.scalars().first()

    # =====================================================
    # CREATE STUDENT
    # =====================================================

    async def create_student(
        self,
        db,
        data,
        user_id,
        school_id,
    ):
        profile = StudentProfile(
            user_id=user_id,
            school_id=school_id,
            **data.model_dump(),
        )

        db.add(profile)

        await db.commit()
        await db.refresh(profile)

        return profile

    # =====================================================
    # CREATE TEACHER
    # =====================================================

    async def create_teacher(
        self,
        db,
        data,
        user_id,
        school_id,
    ):
        profile = TeacherProfile(
            user_id=user_id,
            school_id=school_id,
            **data.model_dump(),
        )

        db.add(profile)

        await db.commit()
        await db.refresh(profile)

        return profile

    # =====================================================
    # CREATE PARENT
    # =====================================================

    async def create_parent(
        self,
        db,
        data,
        user_id,
        school_id,
    ):
        profile = ParentProfile(
            user_id=user_id,
            school_id=school_id,
            **data.model_dump(),
        )

        db.add(profile)

        await db.commit()
        await db.refresh(profile)

        return profile
