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


def create_demo_users(db, school_id):
    users = []

    for i in range(1, 6):
        users.append(
            User(
                email=f"student{i}@demo.com",
                first_name=f"Student{i}",
                last_name="Demo",
                password_hash=hash_password("password123"),
                role=UserRole.STUDENT,
                school_id=school_id,
                is_active=True,
                profile_completed=True,
            )
        )

    for i in range(1, 6):
        users.append(
            User(
                email=f"teacher{i}@demo.com",
                first_name=f"Teacher{i}",
                last_name="Demo",
                password_hash=hash_password("password123"),
                role=UserRole.TEACHER,
                school_id=school_id,
                is_active=True,
                profile_completed=True,
            )
        )

    for i in range(1, 6):
        users.append(
            User(
                email=f"parent{i}@demo.com",
                first_name=f"Parent{i}",
                last_name="Demo",
                password_hash=hash_password("password123"),
                role=UserRole.PARENT,
                school_id=school_id,
                is_active=True,
                profile_completed=True,
            )
        )

    db.add_all(users)
    return users


async def create_school_with_admin():
    async with async_session_local() as db:
        email = "schooladmin@system.com"

        # 1. CHECK ADMIN
        result = await db.execute(select(User).where(User.email == email))
        admin = result.scalar_one_or_none()

        school = None

        # 2. IF ADMIN EXISTS → GET SCHOOL
        if admin:
            print("Admin already exists → using existing school")
            school = await db.get(School, admin.school_id)

        else:
            # CREATE SCHOOL
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
            await db.flush()

            # CREATE ADMIN
            admin = User(
                email=email,
                first_name="System",
                last_name="Admin",
                password_hash=hash_password("SchoolAdmin@12345"),
                role=UserRole.SCHOOL_ADMIN,
                school_id=school.id,
                is_active=True,
                profile_completed=True,
            )

            db.add(admin)

        # 3. ALWAYS SEED DEMO USERS (BUT AVOID DUPLICATES OPTIONAL)
        await db.flush()

        # Optional: prevent duplicate demo users
        existing_demo = await db.execute(
            select(User).where(User.email.like("%@demo.com"))
        )
        if existing_demo.scalars().first():
            print("Demo users already exist → skipping demo seed")
        else:
            create_demo_users(db, school.id)

        await db.commit()

        print("✅ Seed completed")
        print("School ID:", school.id)
        print("Admin ID:", admin.id)


if __name__ == "__main__":
    asyncio.run(create_school_with_admin())
