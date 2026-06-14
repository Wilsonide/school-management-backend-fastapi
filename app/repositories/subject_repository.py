from sqlalchemy import select

from app.models.subject import Subject


class SubjectRepository:

    async def create(self, db, subject):
        db.add(subject)
        await db.commit()
        await db.refresh(subject)
        return subject

    async def get_by_school(self, db, school_id: str):
        result = await db.execute(
            select(Subject).where(Subject.school_id == school_id)
        )
        return result.scalars().all()
    
subject_repo = SubjectRepository()