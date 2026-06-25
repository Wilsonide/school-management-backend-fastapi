from uuid import UUID

from fastapi import HTTPException

from app.models.terms import Term
from app.repositories.term_repository import (
    term_repo,
)


class TermService:
    def __init__(self):
        self.repo = term_repo

    async def create_term(
        self,
        db,
        payload,
        school_id,
    ):
        existing_terms = await self.repo.get_all(
            db,
            school_id,
        )

        term = Term(
            session_id=payload.session_id,
            name=payload.name,
            start_date=payload.start_date,
            end_date=payload.end_date,
            school_id=school_id,
            is_active=len(existing_terms) == 0,
        )

        return await self.repo.create(
            db,
            term,
        )

    async def get_terms(
        self,
        db,
        school_id,
    ):
        terms = await self.repo.get_all(
            db,
            school_id,
        )

        return {
            "terms": [
                {
                    "id": str(term.id),
                    "name": term.name,
                    "session_id": str(term.session_id),
                    "is_active": term.is_active,
                }
                for term in terms
            ],
        }

    async def activate_term(
        self,
        db,
        term_id: UUID,
        school_id: UUID,
    ):
        terms = await self.repo.get_all(
            db,
            school_id,
        )

        target_term = None

        for term in terms:
            if str(term.id) == str(term_id):
                target_term = term

            term.is_active = str(term.id) == str(term_id)

        if not target_term:
            raise HTTPException(
                status_code=404,
                detail="Term not found.",
            )

        await db.commit()

        await db.refresh(target_term)

        return {
            "success": True,
            "message": "Term activated successfully.",
            "term": {
                "id": str(target_term.id),
                "name": target_term.name,
            },
        }


term_service = TermService()
