from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.class_subject_repository import (
    ClassSubjectRepository,
)


class ClassSubjectService:
    def __init__(self):
        self.repo = ClassSubjectRepository()

    async def assign_subject(
        self,
        db: AsyncSession,
        class_id: str,
        subject_id: str,
    ):
        return await self.repo.assign_subject(
            db,
            class_id,
            subject_id,
        )

    async def remove_subject(
        self,
        db: AsyncSession,
        class_id: str,
        subject_id: str,
    ):
        return await self.repo.remove_subject(
            db,
            class_id,
            subject_id,
        )

    async def get_class_subjects(
        self,
        db: AsyncSession,
        class_id: str,
    ):
        subjects = await self.repo.get_class_subjects(
            db,
            class_id,
        )

        return {
            "subjects": [
                {
                    "id": str(subject.id),
                    "name": subject.name,
                }
                for subject in subjects
            ],
        }


class_subject_service = ClassSubjectService()
