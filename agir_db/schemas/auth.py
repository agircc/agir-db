from pydantic import BaseModel, EmailStr
from typing import Optional


class Token(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str


class TokenPayload(BaseModel):
    sub: Optional[str] = None
    jti: Optional[str] = None
    type: Optional[str] = None


class SendVerificationCode(BaseModel):
    email: EmailStr


class VerifyEmail(BaseModel):
    email: EmailStr
    code: str


class RefreshToken(BaseModel):
    refresh_token: str 