from datetime import timedelta
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from models.auth import Token, LoginRequest
from services.auth_service import AuthService
from config import settings

class AuthController:
    @staticmethod
    async def login(login_data: LoginRequest, db: AsyncSession) -> Token:
        auth_service = AuthService(db)
        user = await auth_service.authenticate_user(
            login_data.email, 
            login_data.password
        )
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = auth_service.create_access_token(
            data={"sub": user.email},
            expires_delta=access_token_expires
        )
        
        return Token(access_token=access_token, token_type="bearer")

    @staticmethod
    async def logout(token: str, db: AsyncSession) -> dict:
        auth_service = AuthService(db)
        await auth_service.logout(token)
        return {"message": "Successfully logged out"} 
    
    @staticmethod
    async def refresh_token(token: str, db: AsyncSession) -> Token:
        auth_service = AuthService(db)
        return await auth_service.refresh_token(token)