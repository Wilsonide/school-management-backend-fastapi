from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.class_subject import ClassSubject
from app.models.subject import Subject


class ClassSubjectRepository:
    async def assign_subject(
        self,
        db: AsyncSession,
        class_id: str,
        subject_id: str,
    ):
        existing = await db.scalar(
            select(ClassSubject).where(
                ClassSubject.class_id == class_id,
                ClassSubject.subject_id == subject_id,
            ),
        )

        if existing:
            return existing

        item = ClassSubject(
            class_id=class_id,
            subject_id=subject_id,
        )

        db.add(item)

        await db.commit()

        await db.refresh(item)

        return item

    async def remove_subject(
        self,
        db: AsyncSession,
        class_id: str,
        subject_id: str,
    ):
        await db.execute(
            delete(ClassSubject).where(
                ClassSubject.class_id == class_id,
                ClassSubject.subject_id == subject_id,
            ),
        )

        await db.commit()

        return True

    async def get_class_subjects(
        self,
        db: AsyncSession,
        class_id: str,
    ):
        result = await db.execute(
            select(Subject)
            .join(
                ClassSubject,
                ClassSubject.subject_id == Subject.id,
            )
            .where(
                ClassSubject.class_id == class_id,
            )
            .order_by(Subject.name),
        )

        return result.scalars().all()
