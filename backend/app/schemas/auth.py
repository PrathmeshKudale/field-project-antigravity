from pydantic import BaseModel, Field
from typing import Literal

try:
    from pydantic import EmailStr
    from pydantic.networks import import_email_validator
    import_email_validator()
except Exception:
    EmailStr = str  # type: ignore


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=10, description="Password must be at least 10 characters")
    language: str = "en"
    guardian_consent: bool = Field(description="Consent: 18+ or guardian agreement")


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    language: str


class UserResponse(BaseModel):
    id: str
    email: str
    role: str
    language: str
    allow_storing_questions: bool
