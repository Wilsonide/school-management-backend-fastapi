from app.models.user import User, UserRole
from app.repositories.admin_repository import AdminRepository
from app.repositories.school_repository import SchoolRepository
from app.utils.helper import hash_password


class AdminService:
    def __init__(self):
        self.repo = AdminRepository()
        self.school_repo = SchoolRepository()

    # =====================================
    # DASHBOARD STATS
    # =====================================
    # =====================================
    # GET ALL SCHOOLS
    # =====================================

    async def get_schools(self, db):
        return await self.school_repo.get_schools(db)

    async def create_school_admin(self, db, payload):
        school = await self.school_repo.get_by_id(
            db,
            payload["school_id"],
        )

        if not school:
            return None

        user = User(
            first_name=payload["first_name"],
            last_name=payload["last_name"],
            email=payload["email"],
            password_hash=hash_password(payload["password"]),
            role=UserRole.SCHOOL_ADMIN,
            school_id=school.id,
            profile_completed=True,
        )

        return await self.repo.create_user(db, user)

    # =====================================
    # DELETE ADMIN
    # =====================================
    async def delete_admin(self, db, user_id):
        user = await self.repo.get_user(db, user_id)

        if not user:
            return None

        await self.repo.delete_user(db, user)

        return True

    # =====================================
    # ASSIGN SCHOOL ADMIN (KEEP)
    # =====================================
    async def assign_school_admin(self, db, user_id, school_id):
        user = await self.repo.get_user(db, user_id)
        school = await self.school_repo.get_by_id(db, school_id)

        if not user or not school:
            return None

        user.role = UserRole.SCHOOL_ADMIN
        user.school_id = school.id

        return await self.repo.save_user(db, user)

    async def get_dashboard_stats(self, db):
        schools = await self.repo.count_schools(db)

        users = await self.repo.count_users(db)

        admins = await self.repo.count_school_admins(db)

        return {
            "schools": schools,
            "users": users,
            "admins": admins,
        }

    # =====================================
    # ASSIGN SCHOOL ADMIN
    # =====================================

    # =====================================
    # REVOKE SCHOOL ADMIN
    # =====================================

    async def revoke_school_admin(
        self,
        db,
        user_id,
    ):
        user = await self.repo.get_user(
            db,
            user_id,
        )

        if not user:
            return None

        if user.role != UserRole.SCHOOL_ADMIN:
            return user

        user.role = UserRole.TEACHER

        return await self.repo.save_user(
            db,
            user,
        )

    async def get_admins(self, db):
        return await self.repo.get_admins(db)
