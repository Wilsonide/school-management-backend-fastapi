from app.repositories.school_admin_repository import school_admin_repo
from fastapi import HTTPException

from app.schemas.school_admin import (
    UpdateStudentRequest,
    UpdateTeacherRequest,
    UpdateClassRequest,
    UpdateSubjectRequest,
)


class SchoolAdminService:
    def __init__(self):
        self.repo = school_admin_repo

    # =========================
    # STATS
    # =========================
    async def get_stats(self, db, school_id: str):
        students = await self.repo.count_students(db, school_id)
        teachers = await self.repo.count_teachers(db, school_id)
        classes = await self.repo.count_classes(db, school_id)

        return {
            "students": students,
            "teachers": teachers,
            "classes": classes,
        }

    # =========================
    # STUDENTS
    # =========================
    async def get_students(self, db, school_id: str):
        users = await self.repo.get_students(db, school_id)

        return [
            {
                "id": str(t.id),
                "first_name": t.first_name,
                "last_name": t.last_name,
                "email": t.email,
                "is_active": t.is_active,
                "profile_completed": t.profile_completed,
                "created_at": t.created_at,
            }
            for t in users
        ]

    # =========================
    # TEACHERS
    # =========================
    async def get_teachers(self, db, school_id: str):
        users = await self.repo.get_teachers(db, school_id)

        return [
            {
                "id": str(t.id),
                "first_name": t.first_name,
                "last_name": t.last_name,
                "email": t.email,
                "is_active": t.is_active,
                "profile_completed": t.profile_completed,
                "created_at": t.created_at,
            }
            for t in users
        ]
    async def update_student(
    self,
    db,
    school_id: str,
    student_id: str,
    payload: UpdateStudentRequest,
):
        student = await self.repo.get_student_by_id(
            db,
            school_id,
            student_id,
        )

        if not student:
            raise HTTPException(
                status_code=404,
                detail="Student not found",
            )

        student.first_name = payload.first_name
        student.last_name = payload.last_name
        student.email = payload.email

        await self.repo.commit(db)

        return {
            "message": "Student updated successfully",
        }
    async def update_teacher(
        self,
        db,
        school_id: str,
        teacher_id: str,
        payload: UpdateTeacherRequest,
    ):
        teacher = await self.repo.get_teacher_by_id(
            db,
            school_id,
            teacher_id,
        )

        if not teacher:
            raise HTTPException(
                status_code=404,
                detail="Teacher not found",
            )

        teacher.first_name = payload.first_name
        teacher.last_name = payload.last_name
        teacher.email = payload.email

        await self.repo.commit(db)

        return {
            "message": "Teacher updated successfully",
        }
    
    async def update_class(
    self,
    db,
    school_id: str,
    class_id: str,
    payload: UpdateClassRequest,
):
        school_class = await self.repo.get_class_by_id(
            db,
            school_id,
            class_id,
        )

        if not school_class:
            raise HTTPException(
                status_code=404,
                detail="Class not found",
            )

        school_class.name = payload.name
        school_class.level = payload.level

        await self.repo.commit(db)

        return {
            "message": "Class updated successfully",
        }
    
    async def update_subject(
    self,
    db,
    school_id: str,
    subject_id: str,
    payload: UpdateSubjectRequest,
):
        subject = await self.repo.get_subject_by_id(
            db,
            school_id,
            subject_id,
        )

        if not subject:
            raise HTTPException(
                status_code=404,
                detail="Subject not found",
            )

        subject.name = payload.name

        await self.repo.commit(db)

        return {
            "message": "Subject updated successfully",
        }
    async def delete_subject(
    self,
    db,
    school_id: str,
    subject_id: str,
):
        subject = await self.repo.get_subject_by_id(
            db,
            school_id,
            subject_id,
        )

        if not subject:
            raise HTTPException(
                status_code=404,
                detail="Subject not found",
            )

        await self.repo.delete_subject(
            db,
            subject,
        )

        await self.repo.commit(db)

        return {
            "message": "Subject deleted successfully",
        }
    async def export_results(
    self,
    db,
    school_id: str,
    session_id: str,
    term_id: str,
    class_id: str,
):
        results = await self.result_repo.get_class_results(
            db=db,
            school_id=school_id,
            class_id=class_id,
            session_id=session_id,
            term_id=term_id,
        )

        return results
    
    async def export_attendance(
    self,
    db,
    school_id: str,
    session_id: str,
    term_id: str,
):
        rows = await self.attendance_repo.get_attendance_analytics(
            db=db,
            school_id=school_id,
            session_id=session_id,
            term_id=term_id,
        )

        return rows
school_admin_service = SchoolAdminService()
