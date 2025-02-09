from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User, UserCreate, UserUpdate
from services.user_service import UserService
from typing import List
from utils.auth import get_current_user
from db.models import UserRole
from db.database import get_db

router = APIRouter()

class UserController:
    @staticmethod
    async def get_users_list(current_user: User, db: AsyncSession) -> List[User]:
        if current_user.role != UserRole.ADMIN:
            raise HTTPException(status_code=403, detail="Admin role required")
        user_service = UserService(db)
        return await user_service.get_latest_users(limit=100)

    @staticmethod
    async def create_user(user_data: UserCreate, db: AsyncSession) -> User:
        user_service = UserService(db)
        
        # Check if user already exists
        existing_user = await user_service.get_user_by_email(user_data.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
            
        return await user_service.create_user(user_data)

    @staticmethod
    async def get_user(user_id: int, db: AsyncSession) -> User:
        user_service = UserService(db)
        user = await user_service.get_user(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user 
    
    @staticmethod
    async def update_user(user_id: int, user_data: UserUpdate, db: AsyncSession) -> User:
        user_service = UserService(db)
        return await user_service.update_user(user_id, user_data)