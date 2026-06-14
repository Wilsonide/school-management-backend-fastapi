from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import DBSession, RequireSchoolAdmin
from app.db.database import get_db
from app.services.class_subject_service import class_subject_service
from app.services.school_admin_service import school_admin_service
from app.services.school_assignment_service import school_assignment_service
from app.services.school_class_service import school_class_service
from app.services.timetable_service import timetable_service
from app.schemas.academic_session import (
    AcademicSessionCreate,
)

from app.schemas.term import (
    TermCreate,
)

from app.services.academic_session_service import (
    academic_session_service,
)

from app.services.term_service import (
    term_service,
)

router = APIRouter(
    prefix="/school-admin",
    tags=["School Admin"],
)


# =========================
# STATS
# =========================
@router.get("/stats")
async def get_stats(
    db: Annotated[AsyncSession, Depends(get_db)],
    user: RequireSchoolAdmin,
):
    return await school_admin_service.get_stats(db, str(user.school_id))


@router.post("/classes")
async def create_class(
    payload: dict,
    db: DBSession,
    user: RequireSchoolAdmin,
):
    if not user.school_id:
        raise HTTPException(status_code=400, detail="No school assigned")

    return await school_class_service.create_class(db, payload, user.school_id)


@router.get("/classes")
async def get_classes(
    db: DBSession,
    user: RequireSchoolAdmin,
):
    return await school_class_service.get_classes(db, user.school_id)


@router.delete("/classes/{class_id}")
async def delete_class(
    class_id: str,
    db: DBSession,
    _: RequireSchoolAdmin,
):
    result = await school_class_service.delete_class(db, class_id)

    if not result:
        raise HTTPException(status_code=404, detail="Class not found")

    return {"message": "Class deleted"}


@router.get("/{class_id}/students")
async def get_students(
    class_id: str,
    db: DBSession,
    user: RequireSchoolAdmin,
):
    return await school_assignment_service.get_students(db, user.school_id, class_id)


@router.get("/{class_id}/teachers")
async def get_teachers(class_id: str, db: DBSession, user: RequireSchoolAdmin):
    return await school_assignment_service.get_teachers(
        db,
        user.school_id,
        class_id,
    )


@router.post("/classes/{class_id}/assign-student/{student_id}")
async def assign_student(
    class_id: str,
    student_id: str,
    db: DBSession,
    _: RequireSchoolAdmin,
):
    return await school_assignment_service.assign_student(db, student_id, class_id)


@router.post("/classes/{class_id}/assign-teacher/{teacher_id}")
async def assign_teacher(
    class_id: str,
    teacher_id: str,
    db: DBSession,
    _: RequireSchoolAdmin,
):
    return await school_assignment_service.assign_teacher(db, teacher_id, class_id)


@router.get("/classes/{class_id}/students")
async def class_students(
    class_id: str,
    db: DBSession,
    _: RequireSchoolAdmin,
):
    return await school_assignment_service.get_class_students(db, class_id)


@router.get("/classes/{class_id}/teachers")
async def class_teachers(
    class_id: str,
    db: DBSession,
    _: RequireSchoolAdmin,
):
    return await school_assignment_service.get_class_teachers(db, class_id)


@router.get("/classes/{class_id}/subjects")
async def get_subjects(class_id: str, db: DBSession, _: RequireSchoolAdmin):
    return await class_subject_service.get_class_subjects(db, class_id)


@router.post("/classes/{class_id}/subjects/{subject_id}")
async def assign_subject(
    class_id: str,
    subject_id: str,
    db: DBSession,
    _: RequireSchoolAdmin,
):
    return await class_subject_service.assign_subject(db, class_id, subject_id)


@router.delete("/classes/{class_id}/subjects/{subject_id}")
async def remove_subject(
    class_id: str,
    subject_id: str,
    db: DBSession,
    _: RequireSchoolAdmin,
):
    await class_subject_service.remove_subject(db, class_id, subject_id)

    return {"message": "Removed"}


@router.post("/timetable")
async def create_timetable(
    payload: dict,
    db: DBSession,
    user: RequireSchoolAdmin,
):
    return await timetable_service.create_entry(
        db,
        payload["class_id"],
        payload["subject_id"],
        payload["teacher_id"],
        payload["day_of_week"],
        payload["start_time"],
        payload["end_time"],
        user.school_id,
    )


@router.get("/classes/{class_id}/timetable")
async def get_class_timetable(
    class_id: str,
    db: DBSession,
    _: RequireSchoolAdmin,
):
    return await timetable_service.get_class_timetable(db, class_id)


@router.delete("/timetable/{entry_id}")
async def delete_timetable(
    entry_id: str,
    db: DBSession,
    _: RequireSchoolAdmin,
):
    return await timetable_service.delete_entry(db, entry_id)


@router.post("/subjects")
async def create_subject(
    payload: dict,
    db: DBSession,
    user: RequireSchoolAdmin,
):
    return await class_subject_service.create_subject(
        db,
        payload["name"],
        user.school_id,
    )


@router.delete("/classes/{class_id}/students/{student_id}")
async def remove_student(
    class_id: str,
    student_id: str,
    db: DBSession,
    _: RequireSchoolAdmin,
):
    result = await school_assignment_service.remove_student_from_class(
        db,
        student_id,
        class_id,
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Student not found in class",
        )

    return {"message": "Student removed from class"}

# ======================================= Session ========================================================

@router.post("/sessions")
async def create_session(
    payload: AcademicSessionCreate,
    db: DBSession,
    user: RequireSchoolAdmin,
):
    return await academic_session_service.create_session(
        db,
        payload,
        user.school_id,
    )


@router.get("/sessions")
async def get_sessions(
    db: DBSession,
    user: RequireSchoolAdmin,
):
    return await academic_session_service.get_sessions(
        db,
        user.school_id,
    )
# ======================================= Term ========================================================

@router.post("/terms")
async def create_term(
    payload: TermCreate,
    db: DBSession,
    user: RequireSchoolAdmin,
):
    return await term_service.create_term(
        db,
        payload,
        user.school_id,
    )


@router.get("/terms")
async def get_terms(
    db: DBSession,
    user: RequireSchoolAdmin,
):
    return await term_service.get_terms(
        db,
        user.school_id,
    )