from datetime import date

from pydantic import BaseModel


class AcademicSessionCreate(BaseModel):
    name: str
    start_date: date
    end_date: date


class AcademicSessionUpdate(BaseModel):
    name: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    is_active: bool | None = None