from datetime import datetime

from pydantic import BaseModel, EmailStr


# --- Request schemas (what the client sends) ---


class UserCreate(BaseModel):
    """Fields required to create a new user (same shape as Customer in your example)."""

    full_name: str
    username: str
    email: EmailStr
    password: str
    role: str = "user"


class UserLogin(BaseModel):
    """Fields required to log in."""

    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    """Fields that can be updated — all optional (same pattern as UpdateCustomer)."""

    full_name: str | None = None
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    role: str | None = None


# --- Response schemas ---


class Token(BaseModel):
    """Returned after a successful login."""

    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    """User data returned by the API (password is never included)."""

    id: int
    full_name: str
    username: str
    email: str
    created_at: str | None = None
    role: str
