from uuid import UUID

from pydantic import BaseModel


class PromoteStudentsRequest(BaseModel):
    from_class_id: UUID
    to_class_id: UUID

    from_session_id: UUID
    to_session_id: UUID

class CreateClassRequest(BaseModel):
    name: str
    level: str