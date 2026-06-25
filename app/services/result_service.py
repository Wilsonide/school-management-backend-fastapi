from collections import defaultdict
from datetime import UTC, datetime

from fastapi import HTTPException, status

from app.models.result_approval import ResultApproval
from app.models.result_batch import ResultBatch
from app.models.result_record import ResultRecord
from app.models.result_summary import ResultSummary
from app.repositories.result_repository import result_repository
from app.repositories.teacher_assignment_repository import (
    teacher_assignment_repository,
)
from app.mappers.result_mapper import ResultMapper
from app.schemas.result_responses import ResultBatchStatusResponse


class ResultService:
    def __init__(self):
        self.repo = result_repository
        self.assignment_repo = teacher_assignment_repository

    def calculate_grade(
        self,
        score: int,
    ) -> tuple[str, str]:
        if score >= 70:
            return "A", "Excellent"

        if score >= 60:
            return "B", "Very Good"

        if score >= 50:
            return "C", "Good"

        if score >= 45:
            return "D", "Fair"

        if score >= 40:
            return "E", "Pass"

        return "F", "Fail"

    def generate_positions(
        self,
        student_totals: dict,
    ):
        sorted_students = sorted(
            student_totals.items(),
            key=lambda x: x[1],
            reverse=True,
        )

        positions = {}

        current_position = 0
        previous_score = None

        for index, (student_id, score) in enumerate(
            sorted_students,
            start=1,
        ):
            if score != previous_score:
                current_position = index

            positions[student_id] = current_position

            previous_score = score

        return positions

    async def submit_results(
        self,
        db,
        payload,
        teacher,
    ):
        can_manage = await self.assignment_repo.teacher_can_manage_class(
            db,
            teacher.id,
            payload.class_id,
        )

        if not can_manage:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not assigned to this class.",
            )

        exists = await self.repo.result_exists(
            db,
            teacher.school_id,
            payload.class_id,
            payload.session_id,
            payload.term_id,
        )

        if exists:
            raise HTTPException(
                status_code=400,
                detail="Result already exists.",
            )

        try:
            batch = ResultBatch(
                school_id=teacher.school_id,
                class_id=payload.class_id,
                session_id=payload.session_id,
                term_id=payload.term_id,
                created_by=teacher.id,
                status="SUBMITTED",
            )

            await self.repo.create_batch(
                db,
                batch,
            )

            records = []

            totals = defaultdict(int)

            subject_count = defaultdict(int)

            passed_count = defaultdict(int)

            failed_count = defaultdict(int)

            for student in payload.students:
                for score in student.scores:
                    total = score.ca_score + score.exam_score

                    grade, remark = self.calculate_grade(total)

                    records.append(
                        ResultRecord(
                            school_id=teacher.school_id,
                            batch_id=batch.id,
                            student_id=student.student_id,
                            subject_id=score.subject_id,
                            ca_score=score.ca_score,
                            exam_score=score.exam_score,
                            total_score=total,
                            grade=grade,
                            remark=remark,
                            teacher_comment=score.teacher_comment,
                        )
                    )

                    totals[student.student_id] += total

                    subject_count[student.student_id] += 1

                    if grade == "F":
                        failed_count[student.student_id] += 1
                    else:
                        passed_count[student.student_id] += 1

            await self.repo.create_records(
                db,
                records,
            )

            positions = self.generate_positions(
                totals,
            )

            summaries = []

            for student_id, total_score in totals.items():
                count = subject_count[student_id]

                summaries.append(
                    ResultSummary(
                        school_id=teacher.school_id,
                        batch_id=batch.id,
                        student_id=student_id,
                        total_score=total_score,
                        average_score=(total_score / count),
                        subjects_offered=count,
                        passed_subjects=passed_count[student_id],
                        failed_subjects=failed_count[student_id],
                        position=positions[student_id],
                    )
                )

            await self.repo.create_summaries(
                db,
                summaries,
            )

            await self.repo.create_approval_log(
                db,
                ResultApproval(
                    school_id=teacher.school_id,
                    batch_id=batch.id,
                    action_by=teacher.id,
                    action="SUBMITTED",
                    action_at=datetime.now(
                        UTC,
                    ),
                ),
            )

            await self.repo.commit(db)

            return {
                "batch_id": batch.id,
                "status": batch.status,
                "students": len(
                    payload.students,
                ),
                "records": len(
                    records,
                ),
            }

        except Exception:
            await self.repo.rollback(
                db,
            )
            raise

    async def approve_result(
        self,
        db,
        batch_id,
        admin,
    ):
        batch = await self.repo.get_batch(
            db,
            batch_id,
            admin.school_id,
        )

        if not batch:
            raise HTTPException(
                404,
                "Result batch not found.",
            )

        batch.status = "APPROVED"

        await self.repo.save_batch(
            db,
            batch,
        )

        await self.repo.create_approval_log(
            db,
            ResultApproval(
                school_id=admin.school_id,
                batch_id=batch.id,
                action_by=admin.id,
                action="APPROVED",
                action_at=datetime.now(
                    UTC,
                ),
            ),
        )

        await self.repo.commit(db)

        return ResultBatchStatusResponse(
    batch_id=batch.id,
    status=batch.status,
    message="Result approved successfully",
)

    async def reject_result(
        self,
        db,
        batch_id,
        note,
        admin,
    ):
        batch = await self.repo.get_batch(
            db,
            batch_id,
            admin.school_id,
        )

        if not batch:
            raise HTTPException(
                404,
                "Result batch not found.",
            )

        batch.status = "REJECTED"
        batch.requires_review = True

        await self.repo.save_batch(
            db,
            batch,
        )

        await self.repo.create_approval_log(
            db,
            ResultApproval(
                school_id=admin.school_id,
                batch_id=batch.id,
                action_by=admin.id,
                action="REJECTED",
                note=note,
                action_at=datetime.now(
                    UTC,
                ),
            ),
        )

        await self.repo.commit(db)

        return {
    "batch_id": batch.id,
    "status": batch.status,
    "message": "Result rejected successfully",
}

    async def publish_result(
        self,
        db,
        batch_id,
        admin,
    ):
        batch = await self.repo.get_batch(
            db,
            batch_id,
            admin.school_id,
        )

        if not batch:
            raise HTTPException(
                404,
                "Result batch not found.",
            )

        if batch.status != "APPROVED":
            raise HTTPException(
                400,
                "Result must be approved first.",
            )

        batch.status = "PUBLISHED"
        batch.published_at = datetime.now(
            UTC,
        )

        await self.repo.save_batch(
            db,
            batch,
        )

        await self.repo.create_approval_log(
            db,
            ResultApproval(
                school_id=admin.school_id,
                batch_id=batch.id,
                action_by=admin.id,
                action="PUBLISHED",
                action_at=datetime.now(
                    UTC,
                ),
            ),
        )

        await self.repo.commit(db)

        return {
    "batch_id": batch.id,
    "status": batch.status,
    "message": "Result published successfully",
}

    async def update_teacher_comment(
        self,
        db,
        record_id,
        comment,
    ):
        record = await self.repo.get_record(
            db,
            record_id,
        )

        if not record:
            raise HTTPException(
                status_code=404,
                detail="Result record not found.",
            )

        record.teacher_comment = comment

        await self.repo.update_comment(
            db,
            record,
        )

        await self.repo.commit(db)

        return {
            "message": "Comment updated.",
        }

    async def get_class_results(
        self,
        db,
        school_id,
        class_id,
        session_id,
        term_id,
    ):
        batch = await self.repo.get_class_result_batch(
            db,
            school_id,
            class_id,
            session_id,
            term_id,
        )

        if not batch:
            raise HTTPException(
                404,
                "Result batch not found.",
            )

        return ResultMapper.class_result(
    batch,
)

    async def get_student_result(
        self,
        db,
        student,
        session_id,
        term_id,
    ):
        result = await self.repo.get_student_published_result(
            db,
            student.school_id,
            student.id,
            session_id,
            term_id,
        )

        if not result:
            raise HTTPException(
                404,
                "Result not published.",
            )

        return ResultMapper.student_result(
    result,
)
    async def get_student_result_for_pdf(
    self,
    db,
    student,
    session_id,
    term_id,
):
        result = await self.repo.get_student_published_result(
            db,
            student.school_id,
            student.id,
            session_id,
            term_id,
        )

        if not result:
            raise HTTPException(
                status_code=404,
                detail="Result not published.",
            )

        return {
            "student_name": (
                f"{student.first_name} "
                f"{student.last_name}"
            ),
            "admission_number": getattr(
                student.student_profile,
                "admission_number",
                None,
            ),
            "batch": result["batch"],
            "summary": result["summary"],
            "records": result["records"],
        }
    async def get_approval_history(
        self,
        db,
        batch_id,
        school_id,
    ):
        batch = await self.repo.get_batch(
            db,
            batch_id,
            school_id,
        )

        if not batch:
            raise HTTPException(
                status_code=404,
                detail="Result batch not found.",
            )

        history = await self.repo.get_approval_history(
            db,
            batch_id,
        )

        return ResultMapper.approval_history(
            history,
        )


result_service = ResultService()
