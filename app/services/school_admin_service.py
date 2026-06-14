from app.repositories.school_admin_repository import school_admin_repo


class SchoolAdminService:
    def __init__(self):
        self.repo = school_admin_repo

    # =========================
    # STATS
    # =========================
    async def get_stats(self, db, school_id: str):
        students = await self.repo.count_students(db, school_id)
        teachers = await self.repo.count_teachers(db, school_id)
        classes = await self.repo.count_classes(db, school_id)

        return {
            "students": students,
            "teachers": teachers,
            "classes": classes,
        }

    # =========================
    # STUDENTS
    # =========================
    async def get_students(self, db, school_id: str):
        users = await self.repo.get_students(db, school_id)

        return [
            {
                "id": str(t.id),
                "first_name": t.first_name,
                "last_name": t.last_name,
                "email": t.email,
                "is_active": t.is_active,
                "profile_completed": t.profile_completed,
                "created_at": t.created_at,
            }
            for t in users
        ]

    # =========================
    # TEACHERS
    # =========================
    async def get_teachers(self, db, school_id: str):
        users = await self.repo.get_teachers(db, school_id)

        return [
            {
                "id": str(t.id),
                "first_name": t.first_name,
                "last_name": t.last_name,
                "email": t.email,
                "is_active": t.is_active,
                "profile_completed": t.profile_completed,
                "created_at": t.created_at,
            }
            for t in users
        ]


school_admin_service = SchoolAdminService()
