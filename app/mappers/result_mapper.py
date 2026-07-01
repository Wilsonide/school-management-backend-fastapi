from collections import defaultdict

from app.schemas.result_responses import (
    ApprovalHistoryItem,
    ClassResultResponse,
    ClassStudentResponse,
    ClassSubjectResponse,
    StudentResultResponse,
    SubjectResultResponse,
)


class ResultMapper:
    @staticmethod
    def approval_history(history):
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

    # ======================================================
    # CLASS RESULT SHEET
    # ======================================================

    @staticmethod
    def class_result(batch):
        """
        Batch
            -> Subjects
            -> Students
            -> Subject scores
        """

        grouped = defaultdict(list)

        # collect unique subjects
        subject_map = {}

        for record in batch.records:
            grouped[record.student_id].append(record)

            if record.subject_id not in subject_map:
                subject_map[record.subject_id] = ClassSubjectResponse(
                    subject_id=record.subject_id,
                    subject_name=record.subject.name,
                )

        subjects = sorted(
            subject_map.values(),
            key=lambda x: x.subject_name,
        )

        students = []

        for summary in sorted(
            batch.summaries,
            key=lambda x: x.position,
        ):
            student = summary.student

            student_subjects = []

            for record in sorted(
                grouped.get(student.id, []),
                key=lambda r: r.subject.name,
            ):
                student_subjects.append(
                    SubjectResultResponse(
                        record_id=record.id,
                        subject_id=record.subject_id,
                        subject_name=record.subject.name,
                        ca_score=record.ca_score,
                        exam_score=record.exam_score,
                        total_score=record.total_score,
                        grade=record.grade,
                        remark=record.remark,
                        teacher_comment=record.teacher_comment,
                    )
                )

            students.append(
                ClassStudentResponse(
                    student_id=student.id,
                    student_name=f"{student.first_name} {student.last_name}",
                    total_score=summary.total_score,
                    average_score=summary.average_score,
                    position=summary.position,
                    passed_subjects=summary.passed_subjects,
                    failed_subjects=summary.failed_subjects,
                    subjects=student_subjects,
                )
            )

        return ClassResultResponse(
            batch_id=batch.id,
            class_id=batch.class_id,
            session_id=batch.session_id,
            term_id=batch.term_id,
            status=batch.status,
            editable=batch.status
            in (
                "DRAFT",
                "SUBMITTED",
                "REJECTED",
            ),
            subjects=subjects,
            students=students,
        )

    # ======================================================
    # SINGLE STUDENT RESULT
    # ======================================================

    @staticmethod
    def student_result(result):
        """
        Converts a single student's result into StudentResultResponse.
        """

        summary = result["summary"]
        records = result["records"]

        student = summary.student
        batch = summary.batch

        subjects = []

        for record in sorted(records, key=lambda r: r.subject.name):
            subjects.append(
                SubjectResultResponse(
                    record_id=record.id,
                    subject_id=record.subject_id,
                    subject_name=record.subject.name,
                    ca_score=record.ca_score,
                    exam_score=record.exam_score,
                    total_score=record.total_score,
                    grade=record.grade,
                    remark=record.remark,
                    teacher_comment=record.teacher_comment,
                )
            )

        return StudentResultResponse(
            student_id=student.id,
            student_name=f"{student.first_name} {student.last_name}",
            class_name=batch.school_class.name,
            session_name=batch.session.name,
            term_name=batch.term.name,
            total_score=summary.total_score,
            average_score=summary.average_score,
            position=summary.position,
            passed_subjects=summary.passed_subjects,
            failed_subjects=summary.failed_subjects,
            subjects=subjects,
        )
