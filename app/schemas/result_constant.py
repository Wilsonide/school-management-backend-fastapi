from dataclasses import dataclass


@dataclass
class GradeRule:
    min_score: int
    grade: str
    remark: str


GRADE_RULES = [
    GradeRule(70, "A", "Excellent"),
    GradeRule(60, "B", "Very Good"),
    GradeRule(50, "C", "Good"),
    GradeRule(45, "D", "Fair"),
    GradeRule(40, "E", "Pass"),
    GradeRule(0, "F", "Fail"),
]
