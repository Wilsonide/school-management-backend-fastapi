from app.schemas.result_responses import (
    ApprovalHistoryItem,
    ClassResultResponse,
    ClassStudentResultResponse,
    StudentResultResponse,
    SubjectResultResponse,
)

class ResultMapper:
    @staticmethod
    def approval_history(
        history,
    ):

        return [
            ApprovalHistoryItem(
                id=item.id,
                action=item.action,
                note=item.note,
                action_by=item.action_by,
                action_at=item.action_at,
            )
            for item in history
        ]
    @staticmethod
    def student_result(
        result,
    ):

        summary = result["summary"]

        records = result["records"]

        subjects = [
            SubjectResultResponse(
                subject_id=r.subject_id,
                subject_name=r.subject.name,
                ca_score=r.ca_score,
                exam_score=r.exam_score,
                total_score=r.total_score,
                grade=r.grade,
                remark=r.remark,
                teacher_comment=r.teacher_comment,
            )
            for r in records
        ]

        return StudentResultResponse(
            student_id=summary.student_id,
            total_score=summary.total_score,
            average_score=summary.average_score,
            position=summary.position,
            passed_subjects=summary.passed_subjects,
            failed_subjects=summary.failed_subjects,
            subjects=subjects,
        )
    @staticmethod
    def class_result(
        batch,
    ):

        students = []

        for summary in batch.summaries:

            student = summary.student

            students.append(
                ClassStudentResultResponse(
                    student_id=student.id,
                    student_name=(
                        f"{student.first_name} "
                        f"{student.last_name}"
                    ),
                    total_score=summary.total_score,
                    average_score=summary.average_score,
                    position=summary.position,
                )
            )

        students.sort(
            key=lambda x: x.position,
        )

        return ClassResultResponse(
            batch_id=batch.id,
            class_id=batch.class_id,
            session_id=batch.session_id,
            term_id=batch.term_id,
            status=batch.status,
            students=students,
        )