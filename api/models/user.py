from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
class UserBase(BaseModel):
    email: EmailStr
    full_name: str

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    id: int
    is_active: bool = True
    hashed_password: str
    reset_token: Optional[str] = None
    reset_token_expires: Optional[datetime] = None

    class Config:
        from_attributes = True

class User(UserBase):
    id: int
    is_active: bool = True

    class Config:
        from_attributes = True 