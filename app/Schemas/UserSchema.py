from pydantic import BaseModel

class UserCreate(BaseModel):
    id: int
    full_name: str
    username: str
    email: str
    password: str
    created_at: str
    role: str

class UserResponse(BaseModel):
    id: int
    full_name: str
    username: str
    email: str
    created_at: str
    role: str

    class Config:
        from_attributes = True