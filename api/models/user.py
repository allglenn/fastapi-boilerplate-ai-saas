from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from db.models import UserRole

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
    role: UserRole = UserRole.CLIENT

    class Config:
        from_attributes = True

    __tablename__ = "users"
    
    reset_token = Column(String, nullable=True)
    reset_token_expires = Column(DateTime, nullable=True)

class User(UserBase):
    id: int
    is_active: bool = True
    role: UserRole = UserRole.CLIENT

    class Config:
        from_attributes = True 

class UserUpdate(UserBase):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
