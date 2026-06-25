from datetime import date
from uuid import UUID

from fastapi import APIRouter, Query, status

from app.core.deps import (
    DBSession,
    RequireTeacher,
)
from app.schemas.attendance import (
    AttendanceCreate,
    AttendanceSubmissionResponse,
)
from app.schemas.result_responses import (
    ClassResultResponse,
)
from app.schemas.result_schema import (
    ResultBatchCreate,
    ResultSubmissionResponse,
    UpdateTeacherComment,
)
from app.services.attendance_service import attendance_service
from app.services.dashboard_services import (
    dashboard_service,
)
from app.services.lesson_service import lesson_service
from app.services.result_service import result_service
from app.services.teacher_service import teacher_service

router = APIRouter(
    prefix="/teacher",
    tags=["Teacher Endpoints"],
)


# =====================================================
# LESSONS
# =====================================================


@router.get("/lessons/search")
async def search_lessons(
    class_name: str,
    subject_name: str,
    session_name: str,
    term_name: str,
    db: DBSession,
    _: RequireTeacher,
):
    return await lesson_service.get_lessons_filtered(
        db=db,
        class_name=class_name,
        subject_name=subject_name,
        session_name=session_name,
        term_name=term_name,
    )


# =====================================================
# ATTENDANCE
# =====================================================


@router.post(
    "/attendance",
    response_model=AttendanceSubmissionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def submit_attendance(
    payload: AttendanceCreate,
    db: DBSession,
    user: RequireTeacher,
):
    return await attendance_service.submit_attendance(
        db=db,
        payload=payload,
        teacher=user,
    )


@router.get("/attendance/class")
async def get_class_attendance(
    class_id: UUID,
    session_id: UUID,
    term_id: UUID,
    attendance_date: date,
    db: DBSession,
    user: RequireTeacher,
):
    return await attendance_service.get_class_attendance(
        db=db,
        school_id=user.school_id,
        class_id=class_id,
        session_id=session_id,
        term_id=term_id,
        attendance_date=attendance_date,
    )


# =====================================================
# RESULTS
# =====================================================


@router.post(
    "/results",
    response_model=ResultSubmissionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def submit_results(
    payload: ResultBatchCreate,
    db: DBSession,
    user: RequireTeacher,
):
    return await result_service.submit_results(
        db=db,
        payload=payload,
        teacher=user,
    )


@router.patch(
    "/results/records/{record_id}/comment",
)
async def update_teacher_comment(
    record_id: UUID,
    payload: UpdateTeacherComment,
    db: DBSession,
    _: RequireTeacher,
):
    return await result_service.update_teacher_comment(
        db=db,
        record_id=record_id,
        comment=payload.teacher_comment,
    )


@router.get(
    "/results/class",
    response_model=ClassResultResponse,
)
async def get_class_results(
    class_id: UUID,
    session_id: UUID,
    term_id: UUID,
    db: DBSession,
    user: RequireTeacher,
):
    return await result_service.get_class_results(
        db=db,
        school_id=user.school_id,
        class_id=class_id,
        session_id=session_id,
        term_id=term_id,
    )


@router.get("/dashboard")
async def teacher_dashboard(
    db: DBSession,
    user: RequireTeacher,
):
    return await dashboard_service.teacher_dashboard(
        db=db,
        user=user,
    )


@router.get("/classes")
async def get_teacher_classes(
    db: DBSession,
    current_user: RequireTeacher,
):
    classes = await dashboard_service.get_classes(
        db,
        current_user,
    )

    return {
        "classes": classes,
    }


@router.get("/students")
async def get_students(
    db: DBSession,
    teacher: RequireTeacher,
    class_id: str = Query(...),
):
    students = await teacher_service.get_class_students(
        db, teacher, class_id, teacher.school_id
    )

    return {
        "students": students,
    }


@router.get("/subjects")
async def get_subjects(
    db: DBSession,
    current_user: RequireTeacher,
    class_id: str = Query(...),
):
    subjects = await teacher_service.get_subjects(
        db,
        current_user,
        class_id,
    )

    return {
        "subjects": subjects,
    }
