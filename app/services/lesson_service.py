from app.models.lesson import Lesson
from app.repositories.lesson_repository import lesson_repo
from app.utils.helper import serialize_lesson


class LessonService:

    def __init__(self):
        self.repo = lesson_repo
    async def get_all_lessons(
    self,
    db,
):
        lessons = await self.repo.get_all_lessons(db)

        return {
            "lessons": [
                serialize_lesson(lesson)
                for lesson in lessons
            ],
            "total": len(lessons),
        }


    async def get_lesson_by_id(
        self,
        db,
        lesson_id: str,
    ):
        lesson = await self.repo.get_lesson_by_id(
            db,
            lesson_id,
        )
        return serialize_lesson(lesson)

    async def get_lessons_filtered(
    self,
    db,
    class_name=None,
    subject_name=None,
    session_name=None,
    term_name=None,
):
        lessons = await self.repo.get_lessons_filtered(
            db,
            class_name=class_name,
            subject_name=subject_name,
            session_name=session_name,
            term_name=term_name,
        )

        return {
            "lessons": [
                serialize_lesson(lesson)
                for lesson in lessons
            ],
            "total": len(lessons),
        }
    async def create_lesson(
        self,
        db,
        payload,
        created_by,
    ):
        lesson = Lesson(
            created_by=created_by,

            class_id=payload.class_id,
            subject_id=payload.subject_id,

            session_id=payload.session_id,
            term_id=payload.term_id,

            title=payload.title,
            topic=payload.topic,

            objectives=payload.objectives,
            file_url=payload.file_url,

            is_published=payload.is_published,
        )

        lesson = await self.repo.create(
            db,
            lesson,
        )
        return serialize_lesson(lesson)

    async def update_lesson(
        self,
        db,
        lesson_id,
        payload,
    ):
        lesson = await self.repo.get_by_id(
            db,
            lesson_id,
        )

        if not lesson:
            return None

        if payload.title is not None:
            lesson.title = payload.title

        if payload.topic is not None:
            lesson.topic = payload.topic

        if payload.objectives is not None:
            lesson.objectives = payload.objectives

        if payload.file_url is not None:
            lesson.file_url = payload.file_url

        if payload.is_published is not None:
            lesson.is_published = payload.is_published

        await self.repo.save(db)

        return serialize_lesson(lesson)

lesson_service = LessonService()