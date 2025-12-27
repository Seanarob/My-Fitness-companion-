"""
Authentication schemas
"""
from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    """User registration request"""

    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    """User login request"""

    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """JWT token response"""

    access_token: str
    token_type: str = "bearer"

