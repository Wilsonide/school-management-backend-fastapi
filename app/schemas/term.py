from datetime import date

from pydantic import BaseModel


class TermCreate(BaseModel):
    session_id: str
    name: str
    start_date: date
    end_date: date


class TermUpdate(BaseModel):
    name: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    is_active: bool | None = None