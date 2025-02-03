from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User, UserCreate
from services.user_service import UserService

class UserController:
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