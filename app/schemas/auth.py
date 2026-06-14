from pydantic import BaseModel

from app.schemas.user import UserPublic


class LoginRequest(BaseModel):
    email: str
    password: str


class RegisterRequest(BaseModel):
    email: str
    password: str
    invite_code: str

class ForgotPasswordRequest(BaseModel):
    email: str


class ResetPasswordRequest(BaseModel):
    token: str
    password: str


class RegisterResponse(BaseModel):
    message: str
    user: UserPublic