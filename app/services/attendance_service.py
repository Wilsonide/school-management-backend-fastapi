from collections import Counter

from fastapi import HTTPException, status

from app.mappers.attendance_mapper import AttendanceMapper
from app.models.attendance_record import (
    AttendanceRecord,
    AttendanceStatus,
)
from app.models.attendance_sheet import AttendanceSheet
from app.repositories.academic_session_repository import academic_session_repo
from app.repositories.attendance_repository import (
    attendance_repository,
)
from app.repositories.teacher_assignment_repository import (
    teacher_assignment_repository,
)
from app.repositories.term_repository import term_repo
from app.schemas.attendance import (
    AttendanceAnalyticsResponse,
    ClassAttendanceSummaryResponse,
)


class AttendanceService:
    def __init__(self):
        self.repo = attendance_repository
        self.assignment_repo = teacher_assignment_repository
        self.session_repo = academic_session_repo
        self.term_repo = term_repo

    async def submit_attendance(
        self,
        db,
        payload,
        teacher,
    ):
        can_manage = await self.assignment_repo.teacher_has_class_access(
            db=db,
            teacher_id=teacher.id,
            class_id=payload.class_id,
        )

        if not can_manage:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not assigned to this class.",
            )
        active_session = await self.session_repo.get_active(
            db,
            teacher.school_id,
        )

        active_term = await self.term_repo.get_active(
            db,
            teacher.school_id,
        )
        sheet = await self.repo.get_sheet_by_scope(
            db=db,
            school_id=teacher.school_id,
            class_id=payload.class_id,
            session_id=active_session.id,
            term_id=active_term.id,
            attendance_date=payload.attendance_date,
        )
        if not sheet:
            sheet = AttendanceSheet(
                school_id=teacher.school_id,
                class_id=payload.class_id,
                session_id=active_session.id,
                term_id=active_term.id,
                attendance_date=payload.attendance_date,
                marked_by=teacher.id,
            )

            await self.repo.create_sheet(
                db,
                sheet,
            )
        else:
            await self.repo.delete_sheet_records(
                db,
                sheet.id,
            )
        records = []

        for row in payload.students:
            records.append(
                AttendanceRecord(
                    school_id=teacher.school_id,
                    sheet_id=sheet.id,
                    student_id=row.student_id,
                    status=row.status,
                    note=row.note,
                )
            )
        await self.repo.create_records(
            db,
            records,
        )

        await self.repo.commit(db)

        present_count = sum(1 for r in records if r.status == AttendanceStatus.PRESENT)

        absent_count = sum(1 for r in records if r.status == AttendanceStatus.ABSENT)

        late_count = sum(1 for r in records if r.status == AttendanceStatus.LATE)

        return {
            "sheet_id": sheet.id,
            "created": True,
            "total_students": len(records),
            "present_count": present_count,
            "absent_count": absent_count,
            "late_count": late_count,
            "message": "Attendance submitted successfully",
        }

    async def get_class_attendance(
        self,
        db,
        school_id,
        class_id,
        session_id,
        term_id,
        attendance_date,
    ):
        sheet = await self.repo.get_class_attendance(
            db=db,
            school_id=school_id,
            class_id=class_id,
            session_id=session_id,
            term_id=term_id,
            attendance_date=attendance_date,
        )

        if not sheet:
            raise HTTPException(
                status_code=404,
                detail="Attendance not found.",
            )

        return AttendanceMapper.class_sheet(
            sheet,
        )

    async def get_student_attendance(
        self,
        db,
        student,
        session_id,
        term_id,
    ):
        records = await self.repo.get_student_attendance(
            db=db,
            school_id=student.school_id,
            student_id=student.id,
            session_id=session_id,
            term_id=term_id,
        )

        return AttendanceMapper.student_history(
            records,
        )

    async def get_analytics(
        self,
        db,
        school_id,
        session_id,
        term_id,
    ):
        rows = await self.repo.get_attendance_analytics(
            db=db,
            school_id=school_id,
            session_id=session_id,
            term_id=term_id,
        )

        classes = []

        for row in rows:
            total = row.total or 0

            attendance_rate = (
                round(
                    ((row.present + row.late) / total) * 100,
                    2,
                )
                if total
                else 0
            )

            classes.append(
                ClassAttendanceSummaryResponse(
                    class_id=row.class_id,
                    class_name=row.name,
                    total_students=total,
                    present_count=row.present or 0,
                    absent_count=row.absent or 0,
                    late_count=row.late or 0,
                    attendance_rate=attendance_rate,
                )
            )

        return AttendanceAnalyticsResponse(
            classes=classes,
        )

    async def get_student_term_summary(
        self,
        db,
        student,
        session_id,
        term_id,
    ):
        rows = await self.repo.get_student_term_summary(
            db=db,
            school_id=student.school_id,
            student_id=student.id,
            session_id=session_id,
            term_id=term_id,
        )
        stats = {
            AttendanceStatus.PRESENT: 0,
            AttendanceStatus.ABSENT: 0,
            AttendanceStatus.LATE: 0,
        }

        for status, count in rows:
            stats[status] = count
        total_days = sum(
            stats.values(),
        )

        attendance_rate = 0

        if total_days:
            attendance_rate = round(
                (
                    (stats[AttendanceStatus.PRESENT] + stats[AttendanceStatus.LATE])
                    / total_days
                )
                * 100,
                2,
            )
        return {
            "total_days": total_days,
            "present": stats[AttendanceStatus.PRESENT],
            "absent": stats[AttendanceStatus.ABSENT],
            "late": stats[AttendanceStatus.LATE],
            "attendance_rate": attendance_rate,
        }

    async def get_dashboard(
        self,
        db,
        school_id,
        attendance_date,
    ):
        rows = await self.repo.get_dashboard(
            db,
            school_id,
            attendance_date,
        )

        total_students = await self.repo.get_total_students(
            db,
            school_id,
        )
        counter = Counter()

        for status, count in rows:
            counter[status] = count
        present = counter[AttendanceStatus.PRESENT]

        absent = counter[AttendanceStatus.ABSENT]

        late = counter[AttendanceStatus.LATE]
        attendance_rate = 0

        if total_students:
            attendance_rate = round(
                ((present + late) / total_students) * 100,
                2,
            )
        return {
            "date": attendance_date,
            "total_students": total_students,
            "present": present,
            "absent": absent,
            "late": late,
            "attendance_rate": attendance_rate,
        }


attendance_service = AttendanceService()
