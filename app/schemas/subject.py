from pydantic import BaseModel


class CreateSubjectRequest(BaseModel):
    name: str
    code: str | None = None