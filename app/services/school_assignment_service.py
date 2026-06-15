from app.repositories.school_assignment_repository import school_assignment_repo


class SchoolAssignmentService:
    def __init__(self):
        self.repo = school_assignment_repo

    async def get_students(self, db, school_id: str, class_id: str):
        students = await self.repo.get_school_students_not_in_class(
            db,
            school_id,
            class_id,
        )

        return {
            "students": [
                {
                    "id": str(s.id),
                    "first_name": s.first_name,
                    "last_name": s.last_name,
                    "email": s.email,
                }
                for s in students
            ],
            "count": len(students),
        }

    async def get_school_students(
        self,
        db,
        school_id: str,
    ):
        students = await self.repo.get_school_students(
            db,
            school_id,
        )

        return {
            "students": [
                {
                    "id": str(student.id),
                    "first_name": student.first_name,
                    "last_name": student.last_name,
                    "email": student.email,
                }
                for student in students
            ],
            "count": len(students),
        }

    async def remove_student_from_class(
        self,
        db,
        student_id: str,
        class_id: str,
    ):
        return await self.repo.remove_student_from_class(
            db,
            student_id,
            class_id,
        )

    async def get_teachers(self, db, school_id: str, class_id: str):
        teachers = await self.repo.get_school_teachers_not_in_class(
            db,
            school_id,
            class_id,
        )
        return {
            "teachers": [
                {
                    "id": str(s.id),
                    "first_name": s.first_name,
                    "last_name": s.last_name,
                    "email": s.email,
                }
                for s in teachers
            ],
            "count": len(teachers),
        }

    async def get_school_teachers(
        self,
        db,
        school_id: str,
    ):
        teachers = await self.repo.get_school_teachers(
            db,
            school_id,
        )

        return {
            "teachers": [
                {
                    "id": str(teacher.id),
                    "first_name": teacher.first_name,
                    "last_name": teacher.last_name,
                    "email": teacher.email,
                }
                for teacher in teachers
            ],
            "count": len(teachers),
        }

    async def assign_student(self, db, student_id: str, class_id: str):
        return await self.repo.assign_student(db, student_id, class_id)

    async def assign_teacher(self, db, teacher_id: str, class_id: str):
        return await self.repo.assign_teacher(db, teacher_id, class_id)

    async def get_class_students(self, db, class_id: str):
        students = await self.repo.get_class_students(db, class_id)
        return {
            "students": students,
            "count": len(students),
        }

    async def get_class_teachers(self, db, class_id: str):
        teachers = await self.repo.get_class_teachers(db, class_id)
        return {
            "teachers": teachers,
            "count": len(teachers),
        }


school_assignment_service = SchoolAssignmentService()
