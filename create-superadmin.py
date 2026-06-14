import asyncio
import uuid

from sqlalchemy import select

from app.db.database import async_session_local
from app.models.school import School
from app.models.user import User, UserRole
from app.utils.helper import hash_password


def generate_code():
    return str(uuid.uuid4())[:8].upper()


def generate_slug(name: str):
    return name.lower().replace(" ", "-")


async def create_school_with_admin():
    async with async_session_local() as db:
        email = "schooladmin@system.com"
        password = "SchoolAdmin@12345"

        # 1. Check if admin exists
        result = await db.execute(select(User).where(User.email == email))
        existing = result.scalar_one_or_none()

        if existing:
            print("School admin already exists")
            return

        # 2. Create school (ALL REQUIRED FIELDS INCLUDED)
        school_name = "LERNA International School"

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
        await db.flush()  # generate school.id

        # 3. Create admin linked to school
        user = User(
            email=email,
            first_name="System",
            last_name="Admin",
            password_hash=hash_password(password),
            role=UserRole.SCHOOL_ADMIN,
            school_id=school.id,
            is_active=True,
            profile_completed=True,
        )

        db.add(user)

        await db.commit()
        await db.refresh(user)

        print("✅ School + Admin created successfully")
        print("School ID:", school.id)
        print("Admin ID:", user.id)


if __name__ == "__main__":
    asyncio.run(create_school_with_admin())
