from uuid import UUID

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.result_approval import ResultApproval
from app.models.result_batch import ResultBatch
from app.models.result_record import ResultRecord
from app.models.result_summary import ResultSummary


class ResultRepository:
    # =====================================================
    # WRITE OPERATIONS
    # =====================================================

    async def create_batch(
        self,
        db: AsyncSession,
        batch: ResultBatch,
    ) -> ResultBatch:
        db.add(batch)
        await db.flush()
        return batch

    async def create_records(
        self,
        db: AsyncSession,
        records: list[ResultRecord],
    ) -> list[ResultRecord]:
        db.add_all(records)
        await db.flush()
        return records

    async def create_summaries(
        self,
        db: AsyncSession,
        summaries: list[ResultSummary],
    ) -> list[ResultSummary]:
        db.add_all(summaries)
        await db.flush()
        return summaries

    async def create_approval_log(
        self,
        db: AsyncSession,
        approval: ResultApproval,
    ) -> ResultApproval:
        db.add(approval)
        await db.flush()
        return approval

    async def commit(
        self,
        db: AsyncSession,
    ):
        await db.commit()

    async def rollback(
        self,
        db: AsyncSession,
    ):
        await db.rollback()

    # =====================================================
    # BATCH
    # =====================================================

    async def get_batch(
        self,
        db: AsyncSession,
        batch_id: UUID,
        school_id: UUID,
    ) -> ResultBatch | None:
        result = await db.execute(
            select(ResultBatch).where(
                and_(
                    ResultBatch.id == batch_id,
                    ResultBatch.school_id == school_id,
                )
            )
        )

        return result.scalar_one_or_none()

    async def get_batch_with_records(
        self,
        db: AsyncSession,
        batch_id: UUID,
        school_id: UUID,
    ) -> ResultBatch | None:
        result = await db.execute(
            select(ResultBatch)
            .options(
                selectinload(ResultBatch.records),
                selectinload(ResultBatch.summaries),
                selectinload(ResultBatch.approvals),
            )
            .where(
                and_(
                    ResultBatch.id == batch_id,
                    ResultBatch.school_id == school_id,
                )
            )
        )

        return result.scalar_one_or_none()

    async def get_class_batch(
        self,
        db: AsyncSession,
        school_id: UUID,
        class_id: UUID,
        session_id: UUID,
        term_id: UUID,
    ) -> ResultBatch | None:
        result = await db.execute(
            select(ResultBatch)
            .where(
                and_(
                    ResultBatch.school_id == school_id,
                    ResultBatch.class_id == class_id,
                    ResultBatch.session_id == session_id,
                    ResultBatch.term_id == term_id,
                )
            )
            .order_by(ResultBatch.created_at.desc())
        )

        return result.scalars().first()

    # =====================================================
    # RECORDS
    # =====================================================

    async def get_batch_records(
        self,
        db: AsyncSession,
        batch_id: UUID,
    ) -> list[ResultRecord]:
        result = await db.execute(
            select(ResultRecord)
            .options(
                selectinload(ResultRecord.subject),
                selectinload(ResultRecord.student),
            )
            .where(
                ResultRecord.batch_id == batch_id,
            )
        )

        return list(result.scalars().all())

    async def get_record(
        self,
        db: AsyncSession,
        record_id: UUID,
    ) -> ResultRecord | None:
        result = await db.execute(
            select(ResultRecord).where(ResultRecord.id == record_id)
        )

        return result.scalar_one_or_none()

    async def update_record(
        self,
        db: AsyncSession,
        record: ResultRecord,
    ) -> ResultRecord:
        db.add(record)
        await db.flush()

        return record

    # =====================================================
    # SUMMARYS
    # =====================================================

    async def get_batch_summaries(
        self,
        db: AsyncSession,
        batch_id: UUID,
    ) -> list[ResultSummary]:
        result = await db.execute(
            select(ResultSummary)
            .options(
                selectinload(ResultSummary.student),
            )
            .where(
                ResultSummary.batch_id == batch_id,
            )
            .order_by(ResultSummary.position.asc())
        )

        return list(result.scalars().all())

    async def get_student_summary(
        self,
        db: AsyncSession,
        batch_id: UUID,
        student_id: UUID,
    ) -> ResultSummary | None:
        result = await db.execute(
            select(ResultSummary).where(
                and_(
                    ResultSummary.batch_id == batch_id,
                    ResultSummary.student_id == student_id,
                )
            )
        )

        return result.scalar_one_or_none()

    # =====================================================
    # STUDENT REPORT CARD
    # =====================================================

    async def get_student_records(
        self,
        db: AsyncSession,
        batch_id: UUID,
        student_id: UUID,
    ) -> list[ResultRecord]:
        result = await db.execute(
            select(ResultRecord)
            .options(
                selectinload(ResultRecord.subject),
            )
            .where(
                and_(
                    ResultRecord.batch_id == batch_id,
                    ResultRecord.student_id == student_id,
                )
            )
            .order_by(ResultRecord.subject_id)
        )

        return list(result.scalars().all())

    async def get_student_batch(
        self,
        db: AsyncSession,
        school_id: UUID,
        student_id: UUID,
        session_id: UUID,
        term_id: UUID,
    ) -> ResultBatch | None:
        result = await db.execute(
            select(ResultBatch)
            .join(
                ResultSummary,
                ResultSummary.batch_id == ResultBatch.id,
            )
            .where(
                and_(
                    ResultBatch.school_id == school_id,
                    ResultBatch.session_id == session_id,
                    ResultBatch.term_id == term_id,
                    ResultBatch.status == "PUBLISHED",
                    ResultSummary.student_id == student_id,
                )
            )
        )

        return result.scalar_one_or_none()

    # =====================================================
    # APPROVAL HISTORY
    # =====================================================

    async def get_approval_history(
        self,
        db: AsyncSession,
        batch_id: UUID,
    ) -> list[ResultApproval]:
        result = await db.execute(
            select(ResultApproval)
            .options(
                selectinload(ResultApproval.actor),
            )
            .where(
                ResultApproval.batch_id == batch_id,
            )
            .order_by(ResultApproval.action_at.desc())
        )

        return list(result.scalars().all())

    # =====================================================
    # STATUS
    # =====================================================

    async def save_batch(
        self,
        db: AsyncSession,
        batch: ResultBatch,
    ) -> ResultBatch:
        db.add(batch)
        await db.flush()

        return batch

    # =====================================================
    # EXISTENCE CHECKS
    # =====================================================

    async def result_exists(
        self,
        db: AsyncSession,
        school_id: UUID,
        class_id: UUID,
        session_id: UUID,
        term_id: UUID,
    ) -> bool:
        result = await db.execute(
            select(ResultBatch.id).where(
                and_(
                    ResultBatch.school_id == school_id,
                    ResultBatch.class_id == class_id,
                    ResultBatch.session_id == session_id,
                    ResultBatch.term_id == term_id,
                )
            )
        )

        return result.scalar_one_or_none() is not None

    async def get_class_result_batch(
        self,
        db: AsyncSession,
        school_id: UUID,
        class_id: UUID,
        session_id: UUID,
        term_id: UUID,
    ):
        result = await db.execute(
            select(ResultBatch)
            .options(
                selectinload(ResultBatch.summaries).selectinload(ResultSummary.student)
            )
            .where(
                and_(
                    ResultBatch.school_id == school_id,
                    ResultBatch.class_id == class_id,
                    ResultBatch.session_id == session_id,
                    ResultBatch.term_id == term_id,
                )
            )
        )

        return result.scalar_one_or_none()

    from sqlalchemy.orm import selectinload

    async def get_student_published_result(
        self,
        db: AsyncSession,
        school_id: UUID,
        student_id: UUID,
        session_id: UUID,
        term_id: UUID,
    ):
        result = await db.execute(
            select(ResultBatch)
            .options(
                selectinload(ResultBatch.session),
                selectinload(ResultBatch.term),
                selectinload(ResultBatch.school_class),
            )
            .where(
                and_(
                    ResultBatch.school_id == school_id,
                    ResultBatch.session_id == session_id,
                    ResultBatch.term_id == term_id,
                    ResultBatch.status == "PUBLISHED",
                )
            )
        )

        batch = result.scalar_one_or_none()

        if not batch:
            return None

        records = await self.get_student_records(
            db,
            batch.id,
            student_id,
        )

        summary = await self.get_student_summary(
            db,
            batch.id,
            student_id,
        )

        return {
            "batch": batch,
            "records": records,
            "summary": summary,
        }

    async def update_comment(
        self,
        db: AsyncSession,
        record: ResultRecord,
    ):
        db.add(record)
        await db.flush()
        return record


result_repository = ResultRepository()
