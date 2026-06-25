# app/schemas/academic_response.py

from uuid import UUID

from pydantic import BaseModel


class ActiveSessionResponse(
    BaseModel,
):
    id: UUID
    name: str


class ActiveTermResponse(
    BaseModel,
):
    id: UUID
    name: str


class ActiveAcademicResponse(
    BaseModel,
):
    session: ActiveSessionResponse | None
    term: ActiveTermResponse | None