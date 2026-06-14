from app.models.subject import Subject
from app.repositories.subject_repository import subject_repo


class SubjectService:
    def __init__(self):
        self.repo = subject_repo

    async def create_subject(self, db, name: str, school_id: str):
        subject = Subject(name=name, school_id=school_id)
        return await self.repo.create(db, subject)

    async def get_school_subjects(self, db, school_id: str):
        return await self.repo.get_by_school(db, school_id)


subject_service = SubjectService()
