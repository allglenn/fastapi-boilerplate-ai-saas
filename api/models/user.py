from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    full_name: str

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    id: int
    is_active: bool = True
    hashed_password: str

    class Config:
        from_attributes = True

class User(UserBase):
    id: int
    is_active: bool = True

    class Config:
        from_attributes = True 