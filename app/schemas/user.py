from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional
from uuid import UUID

class UserBase(BaseModel):
    email: EmailStr
    role: str
    school_id: UUID| None 
    first_name: str
    last_name: str

class UserOut(UserBase):
    id: UUID
    profile_completed: bool
    model_config = ConfigDict(from_attributes=True)

class UserPublic(BaseModel):
    id: UUID
    email: EmailStr
    role: str
    school_id: UUID| None = None
    profile_completed: bool
    is_active: bool
    model_config = ConfigDict(from_attributes=True)