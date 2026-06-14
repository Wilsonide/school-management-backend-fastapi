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
        term = Term(
            session_id=payload.session_id,
            name=payload.name,
            start_date=payload.start_date,
            end_date=payload.end_date,
            school_id=school_id,
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
            "terms": terms
        }


term_service = TermService()