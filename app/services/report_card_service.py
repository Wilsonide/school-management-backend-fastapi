from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


class ReportCardService:
    def generate(
        self,
        student,
        result,
        attendance,
    ):
        buffer = BytesIO()

        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
        )

        styles = getSampleStyleSheet()

        elements = []

        summary = result["summary"]
        records = result["records"]
        batch = result["batch"]

        # =========================
        # HEADER
        # =========================

        elements.append(
            Paragraph(
                f"""
                <b>REPORT CARD</b><br/><br/>

                Student: {student.first_name} {student.last_name}<br/>
                Session: {batch.session.name}<br/>
                Term: {batch.term.name}<br/>
                Class: {batch.school_class.name}
                """,
                styles["Title"],
            )
        )

        elements.append(
            Spacer(
                1,
                20,
            )
        )

        # =========================
        # SUBJECT RESULTS
        # =========================

        data = [
            [
                "Subject",
                "CA",
                "Exam",
                "Total",
                "Grade",
            ]
        ]

        for record in records:
            data.append(
                [
                    record.subject.name,
                    record.ca_score,
                    record.exam_score,
                    record.total_score,
                    record.grade,
                ]
            )

        table = Table(data)

        table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.lightgrey,
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        1,
                        colors.black,
                    ),
                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, 0),
                        "Helvetica-Bold",
                    ),
                ]
            )
        )

        elements.append(table)

        elements.append(
            Spacer(
                1,
                20,
            )
        )

        # =========================
        # RESULT SUMMARY
        # =========================

        elements.append(
            Paragraph(
                f"""
                <b>Academic Summary</b><br/><br/>

                Position: {summary.position}<br/>
                Total Score: {summary.total_score}<br/>
                Average Score: {summary.average_score:.2f}<br/>
                Subjects Offered: {summary.subjects_offered}<br/>
                Passed Subjects: {summary.passed_subjects}<br/>
                Failed Subjects: {summary.failed_subjects}
                """,
                styles["Normal"],
            )
        )

        elements.append(
            Spacer(
                1,
                20,
            )
        )

        # =========================
        # ATTENDANCE SUMMARY
        # =========================

        elements.append(
            Paragraph(
                "<b>Attendance Summary</b>",
                styles["Heading2"],
            )
        )

        attendance_data = [
            ["Metric", "Value"],
            ["Present", attendance.present_count],
            ["Absent", attendance.absent_count],
            ["Late", attendance.late_count],
            [
                "Attendance Rate",
                f"{attendance.attendance_rate:.2f}%",
            ],
        ]

        attendance_table = Table(
            attendance_data,
            colWidths=[220, 120],
        )

        attendance_table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.lightgrey,
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        1,
                        colors.black,
                    ),
                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, 0),
                        "Helvetica-Bold",
                    ),
                ]
            )
        )

        elements.append(attendance_table)

        elements.append(
            Spacer(
                1,
                20,
            )
        )

        # =========================
        # TEACHER REMARK
        # =========================

        average = summary.average_score

        if average >= 70:
            remark = "Excellent performance. Keep it up."

        elif average >= 60:
            remark = "Very good performance."

        elif average >= 50:
            remark = "Good performance. More effort required."

        elif average >= 40:
            remark = "Fair performance. Needs improvement."

        else:
            remark = "Poor performance. Serious improvement required."

        elements.append(
            Paragraph(
                f"<b>Teacher's Remark:</b> {remark}",
                styles["Normal"],
            )
        )

        elements.append(
            Spacer(
                1,
                30,
            )
        )

        elements.append(
            Paragraph(
                "_________________________<br/>Class Teacher",
                styles["Normal"],
            )
        )

        doc.build(elements)

        buffer.seek(0)

        return buffer


report_card_service = ReportCardService()