from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    full_name: str
    username: str
    email: EmailStr
    password: str
    role: str = "user"


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    full_name: str | None = None
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    role: str | None = None


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: int
    full_name: str
    username: str
    email: str
    created_at: datetime | None = None
    role: str

    class Config:
        from_attributes = True
