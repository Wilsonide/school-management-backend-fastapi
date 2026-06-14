from sqlalchemy import select

from app.models.student import StudentProfile
from app.models.teacher import TeacherProfile
from app.models.parent import ParentProfile


class ProfileRepository:

    # =====================================================
    # GENERIC SAVE
    # =====================================================
    async def save(self, db, profile):
        db.add(profile)
        await db.commit()
        await db.refresh(profile)
        return profile

    # =====================================================
    # GET STUDENT PROFILE
    # =====================================================
    async def get_student(self, db, user_id):
        result = await db.execute(
            select(StudentProfile).where(
                StudentProfile.user_id == user_id
            )
        )
        return result.scalars().first()

    # =====================================================
    # GET TEACHER PROFILE
    # =====================================================
    async def get_teacher(self, db, user_id):
        result = await db.execute(
            select(TeacherProfile).where(
                TeacherProfile.user_id == user_id
            )
        )
        return result.scalars().first()

    # =====================================================
    # GET PARENT PROFILE
    # =====================================================
    async def get_parent(self, db, user_id):
        result = await db.execute(
            select(ParentProfile).where(
                ParentProfile.user_id == user_id
            )
        )
        return result.scalars().first()

    # =====================================================
    # CREATE STUDENT PROFILE
    # (MATCHES SERVICE: data, user_id, school_id)
    # =====================================================
    async def create_student(self, db, data, user_id, school_id):

        profile = StudentProfile(
            user_id=user_id,
            school_id=school_id,
            **data.model_dump()
        )

        db.add(profile)
        await db.commit()
        await db.refresh(profile)
        return profile

    # =====================================================
    # CREATE TEACHER PROFILE
    # =====================================================
    async def create_teacher(self, db, data, user_id, school_id):

        profile = TeacherProfile(
            user_id=user_id,
            school_id=school_id,
            **data.model_dump()
        )

        db.add(profile)
        await db.commit()
        await db.refresh(profile)
        return profile

    # =====================================================
    # CREATE PARENT PROFILE
    # =====================================================
    async def create_parent(self, db, data, user_id, school_id):

        profile = ParentProfile(
            user_id=user_id,
            school_id=school_id,
            **data.model_dump()
        )

        db.add(profile)
        await db.commit()
        await db.refresh(profile)
        return profile