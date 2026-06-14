from app.models.user import UserRole

from app.models.student import StudentProfile
from app.models.teacher import TeacherProfile
from app.models.parent import ParentProfile

from app.repositories.profile_repository import ProfileRepository

from app.schemas.profiles import StudentProfileCreate, StudentProfileUpdate,TeacherProfileCreate, TeacherProfileUpdate, ParentProfileCreate, ParentProfileUpdate


class ProfileService:
    def __init__(self):
        self.repo = ProfileRepository()

    # =====================================================
    # GET PROFILE
    # =====================================================
    async def get_by_user_id(self, db, user):

        if user.role == UserRole.STUDENT:
            return await self.repo.get_student(db, user.id)

        if user.role == UserRole.TEACHER:
            return await self.repo.get_teacher(db, user.id)

        if user.role == UserRole.PARENT:
            return await self.repo.get_parent(db, user.id)

        return None

    # =====================================================
    # UPDATE PROFILE (ROLE-SCHEMA VALIDATION)
    # =====================================================
    async def update_profile(self, db, user, payload: dict):

        # ---------------- STUDENT ----------------
        if user.role == UserRole.STUDENT:

            data = StudentProfileUpdate(**payload)

            profile = await self.repo.get_student(db, user.id)

            if not profile:
                return None

            for key, value in data.model_dump(exclude_unset=True).items():
                setattr(profile, key, value)

            return await self.repo.save(db, profile)

        # ---------------- TEACHER ----------------
        if user.role == UserRole.TEACHER:

            data = TeacherProfileUpdate(**payload)

            profile = await self.repo.get_teacher(db, user.id)

            if not profile:
                return None

            for key, value in data.model_dump(exclude_unset=True).items():
                setattr(profile, key, value)

            return await self.repo.save(db, profile)

        # ---------------- PARENT ----------------
        if user.role == UserRole.PARENT:

            data = ParentProfileUpdate(**payload)

            profile = await self.repo.get_parent(db, user.id)

            if not profile:
                return None

            for key, value in data.model_dump(exclude_unset=True).items():
                setattr(profile, key, value)

            return await self.repo.save(db, profile)

        return None
    async def create_profile(self, db, user, payload: dict):

        if user.role == "STUDENT":
            data = StudentProfileCreate(**payload)

            profile = await self.repo.create_student(
                db,
                data,
                user.id,
                user.school_id,
            )

        elif user.role == "TEACHER":
            data = TeacherProfileCreate(**payload)

            profile = await self.repo.create_teacher(
                db,
                data,
                user.id,
                user.school_id,
            )

        elif user.role == "PARENT":
            data = ParentProfileCreate(**payload)

            profile = await self.repo.create_parent(
                db,
                data,
                user.id,
                user.school_id,
            )

        # mark completed
        user.profile_completed = True

        db.add(user)
        await db.commit()
        await db.refresh(user)

        return profile