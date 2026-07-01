import os
import tempfile
from datetime import datetime
from io import BytesIO

import requests
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Image,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


class ReportCardService:
    def _download_logo(self, url: str | None):
        """
        Downloads a remote logo temporarily so ReportLab can render it.
        Returns a temp filename or None.
        """

        if not url:
            return None

        try:
            response = requests.get(
                url,
                timeout=10,
            )

            if response.status_code != 200:
                return None

            suffix = os.path.splitext(url)[1] or ".png"

            temp = tempfile.NamedTemporaryFile(
                delete=False,
                suffix=suffix,
            )

            temp.write(response.content)
            temp.close()

            return temp.name

        except Exception:
            return None

    def _teacher_remark(
        self,
        average: float,
    ):
        if average >= 90:
            return "Outstanding performance. Keep striving for excellence."

        if average >= 80:
            return "Excellent performance. Keep it up."

        if average >= 70:
            return "Very good performance. Continue working hard."

        if average >= 60:
            return "Good performance. There is room for improvement."

        if average >= 50:
            return "Fair performance. More effort is required."

        if average >= 40:
            return "Needs improvement. Work harder next term."

        return "Poor performance. Immediate academic improvement is required."

    def _styles(self):
        styles = getSampleStyleSheet()

        styles.add(
            ParagraphStyle(
                name="SchoolName",
                parent=styles["Title"],
                alignment=TA_CENTER,
                fontSize=20,
                leading=24,
                textColor=colors.HexColor("#0F172A"),
                spaceAfter=6,
            )
        )

        styles.add(
            ParagraphStyle(
                name="ReportTitle",
                parent=styles["Heading1"],
                alignment=TA_CENTER,
                fontSize=16,
                leading=18,
                textColor=colors.HexColor("#2563EB"),
                spaceAfter=14,
            )
        )

        styles.add(
            ParagraphStyle(
                name="SmallCenter",
                parent=styles["BodyText"],
                alignment=TA_CENTER,
                fontSize=9,
                leading=12,
            )
        )

        styles.add(
            ParagraphStyle(
                name="SectionTitle",
                parent=styles["Heading2"],
                textColor=colors.HexColor("#1D4ED8"),
                spaceBefore=12,
                spaceAfter=8,
            )
        )

        return styles

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
            leftMargin=30,
            rightMargin=30,
            topMargin=30,
            bottomMargin=30,
        )

        styles = self._styles()

        elements = []

        school = result.get("school", {})
        student_info = result["student"]
        summary = result["summary"]
        subjects = result["subjects"]

        # ======================================================
        # SCHOOL HEADER
        # ======================================================

        logo_path = self._download_logo(
            school.get("logo"),
        )

        if logo_path:
            logo = Image(
                logo_path,
                width=0.8 * inch,
                height=0.8 * inch,
            )

            header = Table(
                [
                    [
                        logo,
                        Paragraph(
                            f"""
                                <b>{school.get("name", "")}</b><br/>
                                {school.get("address", "")}<br/>
                                {school.get("phone", "")}<br/>
                                {school.get("email", "")}
                                """,
                            styles["SchoolName"],
                        ),
                    ]
                ],
                colWidths=[70, 420],
            )

        else:
            header = Table(
                [
                    [
                        Paragraph(
                            f"""
                                <b>{school.get("name", "")}</b><br/>
                                {school.get("address", "")}<br/>
                                {school.get("phone", "")}<br/>
                                {school.get("email", "")}
                                """,
                            styles["SchoolName"],
                        )
                    ]
                ]
            )

        header.setStyle(
            TableStyle(
                [
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
                ]
            )
        )

        elements.append(header)

        elements.append(
            Paragraph(
                "STUDENT REPORT CARD",
                styles["ReportTitle"],
            )
        )

        elements.append(Spacer(1, 12))

        # ======================================================
        # STUDENT INFORMATION
        # ======================================================

        student_table = Table(
            [
                [
                    "Student Name",
                    student_info["name"],
                    "Admission No",
                    student_info["admission_number"] or "-",
                ],
                [
                    "Class",
                    student_info["class_name"],
                    "Session",
                    result["session"],
                ],
                [
                    "Term",
                    result["term"],
                    "Position",
                    summary["position"] or "-",
                ],
            ],
            colWidths=[90, 160, 90, 150],
        )

        student_table.setStyle(
            TableStyle(
                [
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#F3F4F6")),
                    ("BACKGROUND", (2, 0), (2, -1), colors.HexColor("#F3F4F6")),
                    ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                    ("FONTNAME", (2, 0), (2, -1), "Helvetica-Bold"),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                ]
            )
        )

        elements.append(student_table)

        elements.append(Spacer(1, 20))

        # ======================================================
        # SUBJECT RESULTS
        # ======================================================

        elements.append(
            Paragraph(
                "Subject Results",
                styles["SectionTitle"],
            )
        )

        table_data = [
            [
                "Subject",
                "CA",
                "Exam",
                "Total",
                "Grade",
            ]
        ]

        for subject in subjects:
            if isinstance(subject, dict):
                subject_name = subject.get("subject_name", "")
                ca = subject.get("ca_score", 0)
                exam = subject.get("exam_score", 0)
                total = subject.get("total_score", 0)
                grade = subject.get("grade", "-")
            else:
                subject_name = subject.subject_name
                ca = subject.ca_score
                exam = subject.exam_score
                total = subject.total_score
                grade = subject.grade

            table_data.append(
                [
                    subject_name,
                    ca,
                    exam,
                    total,
                    grade,
                ]
            )

        table = Table(
            table_data,
            colWidths=[200, 55, 55, 55, 55],
        )

        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2563EB")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    ("ALIGN", (1, 1), (-1, -1), "CENTER"),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                    ("TOPPADDING", (0, 0), (-1, 0), 8),
                    (
                        "ROWBACKGROUNDS",
                        (0, 1),
                        (-1, -1),
                        [colors.white, colors.HexColor("#F8FAFC")],
                    ),
                ]
            )
        )

        elements.append(table)

        elements.append(Spacer(1, 20))
        # ======================================================
        # ACADEMIC SUMMARY
        # ======================================================

        elements.append(
            Paragraph(
                "Academic Summary",
                styles["SectionTitle"],
            )
        )

        summary_table = Table(
            [
                [
                    "Average Score",
                    f"{summary['average_score']:.2f}",
                    "Total Score",
                    summary["total_score"],
                ],
                [
                    "Position",
                    summary["position"] or "-",
                    "Passed Subjects",
                    summary["passed_subjects"],
                ],
                [
                    "Failed Subjects",
                    summary["failed_subjects"],
                    "",
                    "",
                ],
            ],
            colWidths=[120, 100, 120, 100],
        )

        summary_table.setStyle(
            TableStyle(
                [
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#E8F1FF")),
                    ("BACKGROUND", (2, 0), (2, -1), colors.HexColor("#E8F1FF")),
                    ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                    ("FONTNAME", (2, 0), (2, -1), "Helvetica-Bold"),
                    ("ALIGN", (1, 0), (-1, -1), "CENTER"),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                ]
            )
        )

        elements.append(summary_table)

        elements.append(Spacer(1, 18))

        # ======================================================
        # ATTENDANCE SUMMARY
        # ======================================================

        elements.append(
            Paragraph(
                "Attendance Summary",
                styles["SectionTitle"],
            )
        )

        attendance_table = Table(
            [
                [
                    "Present",
                    attendance.present_count,
                    "Absent",
                    attendance.absent_count,
                ],
                [
                    "Late",
                    attendance.late_count,
                    "Attendance Rate",
                    f"{attendance.attendance_rate:.2f}%",
                ],
            ],
            colWidths=[120, 100, 120, 100],
        )

        attendance_table.setStyle(
            TableStyle(
                [
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#EAFBF0")),
                    ("BACKGROUND", (2, 0), (2, -1), colors.HexColor("#EAFBF0")),
                    ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                    ("FONTNAME", (2, 0), (2, -1), "Helvetica-Bold"),
                    ("ALIGN", (1, 0), (-1, -1), "CENTER"),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                ]
            )
        )

        elements.append(attendance_table)

        elements.append(Spacer(1, 18))

        # ======================================================
        # REMARK
        # ======================================================

        remark = self._teacher_remark(
            summary["average_score"],
        )

        remark_table = Table(
            [
                [
                    Paragraph(
                        f"<b>Teacher's Remark</b><br/><br/>{remark}",
                        styles["BodyText"],
                    )
                ]
            ],
            colWidths=[460],
        )

        remark_table.setStyle(
            TableStyle(
                [
                    ("GRID", (0, 0), (-1, -1), 1, colors.HexColor("#2563EB")),
                    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F8FBFF")),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
                    ("TOPPADDING", (0, 0), (-1, -1), 12),
                    ("LEFTPADDING", (0, 0), (-1, -1), 12),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                ]
            )
        )

        elements.append(remark_table)

        elements.append(Spacer(1, 40))

        # ======================================================
        # SIGNATURES
        # ======================================================

        signatures = Table(
            [
                [
                    "________________________",
                    "",
                    "________________________",
                ],
                [
                    "Class Teacher",
                    "",
                    "Principal",
                ],
            ],
            colWidths=[170, 90, 170],
        )

        signatures.setStyle(
            TableStyle(
                [
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                ]
            )
        )

        elements.append(signatures)

        elements.append(Spacer(1, 25))

        # ======================================================
        # FOOTER
        # ======================================================

        elements.append(
            Paragraph(
                f"""
                    <font size="8" color="grey">
                    Generated on {datetime.now().strftime("%d %B %Y %I:%M %p")}
                    </font>
                    """,
                styles["SmallCenter"],
            )
        )

        doc.build(elements)

        buffer.seek(0)

        return buffer


report_card_service = ReportCardService()
