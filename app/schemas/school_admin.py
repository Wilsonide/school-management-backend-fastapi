from pydantic import BaseModel


class UpdateStudentRequest(BaseModel):
    first_name: str
    last_name: str
    email: str


class UpdateTeacherRequest(BaseModel):
    first_name: str
    last_name: str
    email: str


class UpdateClassRequest(BaseModel):
    name: str
    level: str | None = None


class UpdateSubjectRequest(BaseModel):
    name: str