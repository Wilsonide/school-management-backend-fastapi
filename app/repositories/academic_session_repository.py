from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.academic_session import AcademicSession


class AcademicSessionRepository:

    async def create(
        self,
        db: AsyncSession,
        session: AcademicSession,
    ):
        db.add(session)

        await db.commit()

        await db.refresh(session)

        return session

    async def get_all(
        self,
        db: AsyncSession,
        school_id: str,
    ):
        result = await db.execute(
            select(AcademicSession)
            .where(
                AcademicSession.school_id == school_id
            )
            .order_by(AcademicSession.created_at.desc())
        )

        return result.scalars().all()

    async def get_by_id(
        self,
        db: AsyncSession,
        session_id: str,
    ):
        result = await db.execute(
            select(AcademicSession)
            .where(AcademicSession.id == session_id)
        )

        return result.scalar_one_or_none()

    async def delete(
        self,
        db: AsyncSession,
        session: AcademicSession,
    ):
        await db.delete(session)

        await db.commit()
    async def get_active(
        self,
        db: AsyncSession,
        school_id: str | None = None,
    ):
        query = select(AcademicSession).where(
            AcademicSession.is_active == True
        )

        if school_id:
            query = query.where(
                AcademicSession.school_id == school_id
            )

        result = await db.execute(query)

        return result.scalar_one_or_none()


academic_session_repo = AcademicSessionRepository()