from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.student_class import StudentClass
from app.models.teacher_class import TeacherClass
from app.models.user import User, UserRole


class SchoolAssignmentRepository:
    async def get_school_students(self, db: AsyncSession, school_id: str):
        result = await db.execute(
            select(User).where(
                User.school_id == school_id,
                User.role == UserRole.STUDENT,
            ),
        )
        return result.scalars().all()

    async def get_school_students_not_in_class(
        self,
        db: AsyncSession,
        school_id: str,
        class_id: str,
    ):
        stmt = select(User).where(
            User.school_id == school_id,
            User.role == UserRole.STUDENT,
            ~User.id.in_(
                select(StudentClass.student_id).where(
                    StudentClass.class_id == class_id
                ),
            ),
        )

        result = await db.execute(stmt)
        return result.scalars().all()

    async def get_school_teachers(self, db: AsyncSession, school_id: str):
        result = await db.execute(
            select(User).where(
                User.school_id == school_id,
                User.role == UserRole.TEACHER,
            ),
        )
        return result.scalars().all()

    async def assign_teacher(self, db: AsyncSession, teacher_id: str, class_id: str):
        link = TeacherClass(
            teacher_id=teacher_id,
            class_id=class_id,
        )

        db.add(link)
        await db.commit()
        return link

    async def assign_student(self, db: AsyncSession, student_id: str, class_id: str):
        link = StudentClass(
            student_id=student_id,
            class_id=class_id,
        )

        db.add(link)
        await db.commit()
        return link

    async def get_class_students(self, db: AsyncSession, class_id: str):
        result = await db.execute(
            select(User)
            .join(StudentClass, StudentClass.student_id == User.id)
            .where(StudentClass.class_id == class_id)
        )
        return result.scalars().all()

    async def get_class_teachers(self, db: AsyncSession, class_id: str):
        result = await db.execute(
            select(User)
            .join(TeacherClass, TeacherClass.teacher_id == User.id)
            .where(TeacherClass.class_id == class_id)
        )
        return result.scalars().all()

    async def remove_student_from_class(
        self, db: AsyncSession, student_id: str, class_id: str
    ):
        stmt = delete(StudentClass).where(
            StudentClass.student_id == student_id,
            StudentClass.class_id == class_id,
        )

        result = await db.execute(stmt)
        await db.commit()

        return result.rowcount > 0

    async def get_school_teachers_not_in_class(
        self,
        db: AsyncSession,
        school_id: str,
        class_id: str,
    ):
        stmt = select(User).where(
            User.school_id == school_id,
            User.role == UserRole.TEACHER,
            ~User.id.in_(
                select(TeacherClass.teacher_id).where(TeacherClass.class_id == class_id)
            ),
        )

        result = await db.execute(stmt)
        return result.scalars().all()


school_assignment_repo = SchoolAssignmentRepository()
