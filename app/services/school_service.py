import secrets

from slugify import slugify

from app.models.school import School
from app.models.user import User, UserRole
from app.repositories.school_repository import SchoolRepository
from app.repositories.user_repository import UserRepository
from app.utils.helper import hash_password


class SchoolAlreadyExistsError(Exception):
    pass


class SchoolService:
    def __init__(self):
        self.repo = SchoolRepository()
        self.user_repo = UserRepository()

    async def onboard_school(
        self,
        db,
        payload,
    ):
        slug = slugify(
            payload.school_name,
        )

        existing = await self.repo.get_by_slug(
            db,
            slug,
        )

        if existing:
            raise SchoolAlreadyExistsError(
                "School already exists",
            )

        school_code = f"SCH-{secrets.token_hex(3).upper()}"

        school = School(
            name=payload.school_name,
            slug=slug,
            email=payload.admin_email,
            phone=payload.phone,
            address=payload.address,
            state=payload.state,
            website=payload.website,
            description=payload.description,
            whatsapp_number=payload.whatsapp_number,
            average_fee_range=payload.average_fee_range,
            population_range=payload.population_range,
            referral_source=payload.referral_source,
            code=school_code,
        )

        db.add(school)

        await db.flush()
        existing_user = await self.user_repo.get_by_email(
            db,
            payload.admin_email,
        )

        if existing_user:
            raise SchoolAlreadyExistsError(
                "Email already exists",
            )

        admin = User(
            first_name=payload.admin_first_name,
            last_name=payload.admin_last_name,
            email=payload.admin_email,
            username="admin",
            password_hash=hash_password(payload.admin_password),
            role=UserRole.SCHOOL_ADMIN,
            school_id=school.id,
            profile_completed=True,
        )

        db.add(admin)

        await db.commit()

        await db.refresh(school)

        return {
            "school": school,
            "admin": admin,
        }

    async def get_by_id(
        self,
        db,
        school_id,
    ):
        return await self.repo.get_by_id(
            db,
            school_id,
        )

    async def get_by_slug(
        self,
        db,
        slug,
    ):
        return await self.repo.get_by_slug(
            db,
            slug,
        )

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
