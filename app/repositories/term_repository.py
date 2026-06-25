from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.terms import Term


class TermRepository:

    async def create(
        self,
        db: AsyncSession,
        term: Term,
    ):
        db.add(term)

        await db.commit()

        await db.refresh(term)

        return term

    async def get_all(
        self,
        db: AsyncSession,
        school_id: str,
    ):
        result = await db.execute(
            select(Term)
            .where(Term.school_id == school_id)
            .order_by(Term.created_at.desc())
        )

        return result.scalars().all()

    async def get_session_terms(
        self,
        db: AsyncSession,
        session_id: str,
    ):
        result = await db.execute(
            select(Term)
            .where(Term.session_id == session_id)
        )

        return result.scalars().all()
    async def get_active(
        self,
        db: AsyncSession,
        school_id: str | None = None,
    ):
        query = select(Term).where(
            Term.is_active == True
        )

        if school_id:
            query = query.where(
                Term.school_id == school_id
            )

        result = await db.execute(query)

        return result.scalar_one_or_none()


term_repo = TermRepository()