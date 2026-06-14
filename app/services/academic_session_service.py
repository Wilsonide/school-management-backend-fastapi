from app.models.academic_session import AcademicSession
from app.repositories.academic_session_repository import (
    academic_session_repo,
)


class AcademicSessionService:

    def __init__(self):
        self.repo = academic_session_repo

    async def create_session(
        self,
        db,
        payload,
        school_id,
    ):
        session = AcademicSession(
            name=payload.name,
            start_date=payload.start_date,
            end_date=payload.end_date,
            school_id=school_id,
        )

        return await self.repo.create(
            db,
            session,
        )

    async def get_sessions(
        self,
        db,
        school_id,
    ):
        sessions = await self.repo.get_all(
            db,
            school_id,
        )

        return {
            "sessions": sessions
        }


academic_session_service = AcademicSessionService()