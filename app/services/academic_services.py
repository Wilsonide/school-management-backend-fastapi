# app/services/academic_service.py

from app.repositories.academic_session_repository import (
    academic_session_repo,
)
from app.repositories.term_repository import (
    term_repo,
)


class AcademicService:
    def __init__(self):
        self.session_repo = academic_session_repo
        self.term_repo = term_repo

    async def get_active_period(
        self,
        db,
        school_id,
    ):
        session = await self.session_repo.get_active(
            db,
            school_id,
        )

        term = await self.term_repo.get_active(
            db,
            school_id,
        )

        return {
            "session": (
                {
                    "id": str(session.id),
                    "name": session.name,
                }
                if session
                else None
            ),
            "term": (
                {
                    "id": str(term.id),
                    "name": term.name,
                }
                if term
                else None
            ),
        }


academic_service = AcademicService()
