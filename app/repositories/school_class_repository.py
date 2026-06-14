from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.classes import Class
from app.models.student_class import StudentClass
from app.models.subject import Subject
from app.models.teacher_class import TeacherClass
from app.models.timetable import Timetable


class SchoolClassRepository:
    async def get_class_dashboard(
        self,
        db,
        class_id,
    ):
        cls = await db.get(Class, class_id)

        if not cls:
            return None

        students_count = await db.scalar(
            select(func.count())
            .select_from(StudentClass)
            .where(StudentClass.class_id == class_id),
        )

        teachers_count = await db.scalar(
            select(func.count())
            .select_from(TeacherClass)
            .where(TeacherClass.class_id == class_id),
        )

        subjects_count = await db.scalar(
            select(func.count())
            .select_from(Subject)
            .where(Subject.school_id == cls.school_id),
        )

        timetable_count = await db.scalar(
            select(func.count())
            .select_from(Timetable)
            .where(Timetable.class_id == class_id),
        )

        return {
            "id": str(cls.id),
            "name": cls.name,
            "level": cls.level,
            "students_count": students_count or 0,
            "teachers_count": teachers_count or 0,
            "subjects_count": subjects_count or 0,
            "timetable_count": timetable_count or 0,
        }

    async def create(self, db: AsyncSession, cls: Class):
        db.add(cls)
        await db.commit()
        await db.refresh(cls)
        return cls

    async def get_by_school(self, db: AsyncSession, school_id: str):
        result = await db.execute(
            select(Class)
            .where(Class.school_id == school_id)
            .order_by(Class.created_at.desc()),
        )
        return result.scalars().all()

    async def delete(self, db: AsyncSession, class_id: str):
        result = await db.get(Class, class_id)

        if not result:
            return None

        await db.delete(result)
        await db.commit()
        return True
