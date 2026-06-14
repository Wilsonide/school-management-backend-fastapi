import secrets

from app.models.school import School
from app.models.user import UserRole
from app.repositories.school_repository import SchoolRepository
from app.repositories.user_repository import UserRepository


class SchoolService:
    def __init__(self):
        self.repo = SchoolRepository()
        self.user_repo = UserRepository()

    # =====================================================
    # CREATE SCHOOL
    # =====================================================
    async def create_school(self, db, payload):
        code = f"SCH-{secrets.token_hex(3).upper()}"

        school = School(
            name=payload["name"],
            email=payload["email"],
            phone=payload["phone"],
            address=payload.get("address"),
            website=payload.get("website"),
            slug=payload["name"].lower().replace(" ", "-"),
            code=code,
        )

        return await self.repo.create(
            db,
            school,
        )

    # =====================================================
    # GET ALL SCHOOLS
    # =====================================================
    async def get_schools(self, db):
        schools = await self.repo.get_all(db)

        return schools

    # =====================================================
    # DELETE SCHOOL
    # =====================================================
    async def delete_school(self, db, school_id):
        school = await self.repo.get_by_id(
            db,
            school_id,
        )

        if not school:
            return False

        await self.repo.delete(
            db,
            school,
        )

        return True

    # =====================================================
    # ASSIGN ADMIN
    # =====================================================
    async def assign_admin(
        self,
        db,
        school_id,
        user_id,
    ):
        school = await self.repo.get_by_id(
            db,
            school_id,
        )

        if not school:
            return None

        user = await self.user_repo.get_by_id(
            db,
            user_id,
        )

        if not user:
            return None

        user.role = UserRole.SCHOOL_ADMIN

        user.school_id = school.id

        db.add(user)

        await db.commit()

        await db.refresh(user)

        return user
