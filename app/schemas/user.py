from pydantic import BaseModel, EmailStr
from typing import Optional


# Shared Base Schema
class UserBase(BaseModel):
    username: str
    email: EmailStr



# Request Schemas
class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None


class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True   # SQLAlchemy → Pydantic
