from datetime import date

from sqlalchemy import and_, delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.attendance_record import (
    AttendanceRecord,
    AttendanceStatus,
)
from app.models.attendance_sheet import AttendanceSheet
from app.models.enrollment import StudentEnrollment
from sqlalchemy import case
from app.models.classes import Class

class AttendanceRepository:

    # =====================================================
    # TRANSACTION HELPERS
    # =====================================================

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

    async def create_sheet(
        self,
        db: AsyncSession,
        sheet: AttendanceSheet,
    ):
        db.add(sheet)

        await db.flush()

        return sheet
    async def delete_sheet_records(
        self,
        db: AsyncSession,
        sheet_id,
    ):
        await db.execute(
            delete(AttendanceRecord).where(
                AttendanceRecord.sheet_id == sheet_id,
            )
        )
    async def create_records(
        self,
        db: AsyncSession,
        records: list[AttendanceRecord],
    ):
        db.add_all(records)

        await db.flush()

        return records
    
    async def get_sheet_by_scope(
        self,
        db: AsyncSession,
        school_id,
        class_id,
        session_id,
        term_id,
        attendance_date: date,
    ):
        result = await db.execute(
            select(AttendanceSheet)
            .where(
                and_(
                    AttendanceSheet.school_id == school_id,
                    AttendanceSheet.class_id == class_id,
                    AttendanceSheet.session_id == session_id,
                    AttendanceSheet.term_id == term_id,
                    AttendanceSheet.attendance_date == attendance_date,
                )
            )
        )

        return result.scalar_one_or_none()
    
    async def get_sheet(
        self,
        db: AsyncSession,
        sheet_id,
    ):
        result = await db.execute(
            select(AttendanceSheet)
            .options(
                selectinload(
                    AttendanceSheet.records,
                )
            )
            .where(
                AttendanceSheet.id == sheet_id,
            )
        )

        return result.scalar_one_or_none()
    
    async def get_class_attendance(
        self,
        db: AsyncSession,
        school_id,
        class_id,
        session_id,
        term_id,
        attendance_date,
    ):
        result = await db.execute(
            select(AttendanceSheet)
            .options(
                selectinload(
                    AttendanceSheet.records,
                ).selectinload(
                    AttendanceRecord.student,
                )
            )
            .where(
                and_(
                    AttendanceSheet.school_id == school_id,
                    AttendanceSheet.class_id == class_id,
                    AttendanceSheet.session_id == session_id,
                    AttendanceSheet.term_id == term_id,
                    AttendanceSheet.attendance_date
                    == attendance_date,
                )
            )
        )

        return result.scalar_one_or_none()
    async def get_student_attendance(
        self,
        db: AsyncSession,
        school_id,
        student_id,
        session_id,
        term_id,
    ):
        result = await db.execute(
            select(AttendanceRecord)
            .join(
                AttendanceSheet,
                AttendanceSheet.id
                == AttendanceRecord.sheet_id,
            )
            .options(
                selectinload(
                    AttendanceRecord.sheet,
                )
            )
            .where(
                and_(
                    AttendanceRecord.student_id == student_id,
                    AttendanceSheet.school_id == school_id,
                    AttendanceSheet.session_id == session_id,
                    AttendanceSheet.term_id == term_id,
                )
            )
            .order_by(
                AttendanceSheet.attendance_date.desc(),
            )
        )

        return result.scalars().all()
    

    async def get_student_term_summary(
        self,
        db: AsyncSession,
        school_id,
        student_id,
        session_id,
        term_id,
    ):
        result = await db.execute(
            select(
                AttendanceRecord.status,
                func.count(
                    AttendanceRecord.id,
                ),
            )
            .join(
                AttendanceSheet,
                AttendanceSheet.id
                == AttendanceRecord.sheet_id,
            )
            .where(
                and_(
                    AttendanceRecord.student_id == student_id,
                    AttendanceSheet.school_id == school_id,
                    AttendanceSheet.session_id == session_id,
                    AttendanceSheet.term_id == term_id,
                )
            )
            .group_by(
                AttendanceRecord.status,
            )
        )

        return result.all()
    
    async def get_dashboard(
        self,
        db: AsyncSession,
        school_id,
        attendance_date,
    ):
        result = await db.execute(
            select(
                AttendanceRecord.status,
                func.count(
                    AttendanceRecord.id,
                ),
            )
            .join(
                AttendanceSheet,
                AttendanceSheet.id
                == AttendanceRecord.sheet_id,
            )
            .where(
                and_(
                    AttendanceSheet.school_id
                    == school_id,
                    AttendanceSheet.attendance_date
                    == attendance_date,
                )
            )
            .group_by(
                AttendanceRecord.status,
            )
        )

        return result.all()
    async def get_attendance_analytics(
    self,
    db: AsyncSession,
    school_id,
    session_id,
    term_id,
):
        result = await db.execute(
            select(
                AttendanceSheet.class_id,
                Class.name,

                func.count(
                    AttendanceRecord.id,
                ).label("total"),

                func.sum(
                    case(
                        (
                            AttendanceRecord.status
                            == AttendanceStatus.PRESENT,
                            1,
                        ),
                        else_=0,
                    )
                ).label("present"),

                func.sum(
                    case(
                        (
                            AttendanceRecord.status
                            == AttendanceStatus.ABSENT,
                            1,
                        ),
                        else_=0,
                    )
                ).label("absent"),

                func.sum(
                    case(
                        (
                            AttendanceRecord.status
                            == AttendanceStatus.LATE,
                            1,
                        ),
                        else_=0,
                    )
                ).label("late"),
            )
            .join(
                AttendanceSheet,
                AttendanceSheet.id
                == AttendanceRecord.sheet_id,
            )
            .join(
                Class,
                Class.id
                == AttendanceSheet.class_id,
            )
            .where(
                AttendanceSheet.school_id == school_id,
                AttendanceSheet.session_id == session_id,
                AttendanceSheet.term_id == term_id,
            )
            .group_by(
                AttendanceSheet.class_id,
                Class.name,
            )
            .order_by(
                Class.name,
            )
        )

        return result.all()
    
    async def get_total_students(
        self,
        db: AsyncSession,
        school_id,
    ):
        result = await db.execute(
            select(
                func.count(
                    StudentEnrollment.id,
                )
            )
            .where(
                StudentEnrollment.school_id
                == school_id,
            )
        )

        return result.scalar() or 0
    
attendance_repository = AttendanceRepository()
