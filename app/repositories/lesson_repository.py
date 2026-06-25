from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.academic_session import AcademicSession
from app.models.lesson import Lesson


class LessonRepository:

    async def _base_query(self, db):
        return select(Lesson).options(
            selectinload(Lesson.class_obj),
            selectinload(Lesson.subject),
            selectinload(Lesson.session),
            selectinload(Lesson.term),
        )

    async def create(
        self,
        db,
        lesson,
    ):
        db.add(lesson)

        await db.commit()

        await db.refresh(lesson)

        return lesson

    async def get_by_id(
        self,
        db,
        lesson_id,
    ):
        result = await db.execute(
            select(Lesson).where(
                Lesson.id == lesson_id
            )
        )

        return result.scalar_one_or_none()

    async def save(self, db):
        await db.commit()

    async def get_all_lessons(self, db):
        result = await db.execute(
            (await self._base_query(db))
            .order_by(Lesson.created_at.desc())
        )
        return result.scalars().all()

    async def get_lesson_by_id(self, db, lesson_id: str):
        result = await db.execute(
            (await self._base_query(db))
            .where(Lesson.id == lesson_id)
        )
        return result.scalar_one_or_none()


    async def get_lessons_filtered(
    self,
    db,
    class_name=None,
    subject_name=None,
    session_name=None,
    term_name=None,
):
        query = await self._base_query(db)

        if class_name:
            query = query.where(Lesson.class_obj.has(name=class_name))

        if subject_name:
            query = query.where(Lesson.subject.has(name=subject_name))

        if session_name:
            query = query.where(Lesson.session.has(name=session_name))

        if term_name:
            query = query.where(Lesson.term.has(name=term_name))

        query = query.order_by(Lesson.created_at.desc())

        result = await db.execute(query)

        return result.scalars().all()

lesson_repo = LessonRepository()