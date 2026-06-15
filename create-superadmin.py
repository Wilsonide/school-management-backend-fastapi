import asyncio
import uuid

from sqlalchemy import select

from app.db.database import async_session_local
from app.models.school import School
from app.models.user import User, UserRole
from app.utils.helper import hash_password


# =========================
# HELPERS
# =========================
def generate_code():
    return str(uuid.uuid4())[:8].upper()


def generate_slug(name: str):
    return name.lower().replace(" ", "-")


async def user_exists(db, email: str):
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


# =========================
# SEED FUNCTION
# =========================
async def seed_all():
    async with async_session_local() as db:
        # =========================
        # 1. SUPER ADMIN
        # =========================
        super_admin_email = "superadmin@system.com"

        if not await user_exists(db, super_admin_email):
            super_admin = User(
                email=super_admin_email,
                first_name="Super",
                last_name="Admin",
                password_hash=hash_password("SuperAdmin@12345"),
                role=UserRole.SUPER_ADMIN,
                school_id=None,
                is_active=True,
                profile_completed=True,
            )
            db.add(super_admin)
            print("✅ Super Admin created")

        # =========================
        # 2. SCHOOL
        # =========================
        school_name = "LERNA International School"

        result = await db.execute(
            select(School).where(School.slug == generate_slug(school_name))
        )
        school = result.scalar_one_or_none()

        if not school:
            school = School(
                name=school_name,
                slug=generate_slug(school_name),
                email="info@lerna.com",
                phone="08000000000",
                address="Main Campus",
                website=None,
                logo_url=None,
                subscription_plan="basic",
                code=generate_code(),
                is_active=True,
            )
            db.add(school)
            await db.flush()
            print("✅ School created")

        # =========================
        # 3. SCHOOL ADMIN
        # =========================
        school_admin_email = "schooladmin@system.com"

        if not await user_exists(db, school_admin_email):
            school_admin = User(
                email=school_admin_email,
                first_name="School",
                last_name="Admin",
                password_hash=hash_password("SchoolAdmin@12345"),
                role=UserRole.SCHOOL_ADMIN,
                school_id=school.id,
                is_active=True,
                profile_completed=True,
            )
            db.add(school_admin)
            print("✅ School Admin created")

        # =========================
        # 4. TEACHERS (5)
        # =========================
        for i in range(1, 6):
            email = f"teacher{i}@school.com"

            if not await user_exists(db, email):
                teacher = User(
                    email=email,
                    first_name=f"Teacher{i}",
                    last_name="User",
                    password_hash=hash_password("password123"),
                    role=UserRole.TEACHER,
                    school_id=school.id,
                    is_active=True,
                    profile_completed=True,
                )
                db.add(teacher)

        print("✅ 5 Teachers created (if not existing)")

        # =========================
        # 5. STUDENTS (5)
        # =========================
        for i in range(1, 6):
            email = f"student{i}@school.com"

            if not await user_exists(db, email):
                student = User(
                    email=email,
                    first_name=f"Student{i}",
                    last_name="User",
                    password_hash=hash_password("password123"),
                    role=UserRole.STUDENT,
                    school_id=school.id,
                    is_active=True,
                    profile_completed=True,
                )
                db.add(student)

        print("✅ 5 Students created (if not existing)")

        # =========================
        # 6. PARENTS (5)
        # =========================
        for i in range(1, 6):
            email = f"parent{i}@school.com"

            if not await user_exists(db, email):
                parent = User(
                    email=email,
                    first_name=f"Parent{i}",
                    last_name="User",
                    password_hash=hash_password("password123"),
                    role=UserRole.PARENT,
                    school_id=school.id,
                    is_active=True,
                    profile_completed=True,
                )
                db.add(parent)

        print("✅ 5 Parents created (if not existing)")

        # =========================
        # COMMIT ALL
        # =========================
        await db.commit()
        print("\n🚀 SEED COMPLETED SUCCESSFULLY")


if __name__ == "__main__":
    asyncio.run(seed_all())
