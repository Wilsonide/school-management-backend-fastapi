from uuid import UUID

from fastapi import HTTPException

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
        existing_sessions = await self.repo.get_all(
            db,
            school_id,
        )
        session = AcademicSession(
            name=payload.name,
            start_date=payload.start_date,
            end_date=payload.end_date,
            school_id=school_id,
            is_active=len(existing_sessions) == 0,
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
            "sessions": [
                {
                    "id": str(session.id),
                    "name": session.name,
                    "start_date": session.start_date,
                    "end_date": session.end_date,
                    "is_active": session.is_active,
                }
                for session in sessions
            ]
        }

    async def activate_session(
        self,
        db,
        session_id: UUID,
        school_id: UUID,
    ):
        sessions = await self.repo.get_all(
            db,
            school_id,
        )

        target_session = None

        for session in sessions:
            if str(session.id) == str(session_id):
                target_session = session

            session.is_active = str(session.id) == str(session_id)

        if not target_session:
            raise HTTPException(
                status_code=404,
                detail="Academic session not found.",
            )

        await db.commit()

        await db.refresh(target_session)

        return {
            "success": True,
            "message": "Academic session activated successfully.",
            "session": {
                "id": str(target_session.id),
                "name": target_session.name,
            },
        }


academic_session_service = AcademicSessionService()
