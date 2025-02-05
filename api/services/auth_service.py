from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from models.auth import Token, TokenData
from models.user import User, UserInDB
from services.user_service import UserService
from services.token_blacklist import TokenBlacklistService
from utils.security import verify_password
from config import settings
from models.user import User
import secrets
from services.mail_service import MailService

class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_service = UserService(db)
        self.token_blacklist = TokenBlacklistService(db)

    async def authenticate_user(self, email: str, password: str) -> User | None:
        user = await self.user_service.get_user_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return User(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            is_active=user.is_active
        )

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, 
            settings.SECRET_KEY, 
            algorithm=settings.ALGORITHM
        )
        return encoded_jwt

    async def get_current_user(self, token: str) -> User:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        # Check if token is blacklisted
        if await self.token_blacklist.is_token_blacklisted(token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has been revoked",
                headers={"WWW-Authenticate": "Bearer"},
            )

        try:
            payload = jwt.decode(
                token, 
                settings.SECRET_KEY, 
                algorithms=[settings.ALGORITHM]
            )
            email: str = payload.get("sub")
            if email is None:
                raise credentials_exception
            token_data = TokenData(email=email)
        except JWTError:
            raise credentials_exception
        
        user = await self.user_service.get_user_by_email(email=token_data.email)
        if user is None:
            raise credentials_exception
        return user 

    async def logout(self, token: str) -> None:
        await self.token_blacklist.blacklist_token(token) 
    
    async def refresh_token(self, token: str) -> Token:
        user = await self.get_current_user(token)
        await self.token_blacklist.blacklist_token(token) 
        new_token = self.create_access_token(data={"sub": user.email})
        return Token(access_token=new_token, token_type="bearer")

    async def create_password_reset_token(self, email: str) -> bool:
        user = await self.user_service.get_user_by_email(email)
        if not user:
            return False
        
        # Generate reset token
        reset_token = secrets.token_urlsafe(32)
        expiration = datetime.utcnow() + timedelta(hours=24)
        
        # Store reset token in database
        user.reset_token = reset_token
        user.reset_token_expires = expiration
        await self.db.commit()

        # Send email
        mail_service = MailService()
        reset_link = f"{settings.DOMAIN_NAME}/reset-password?token={reset_token}"
        html_content = f"""
        <h2>Password Reset Request</h2>
        <p>Click the link below to reset your password:</p>
        <p><a href="{reset_link}">{reset_link}</a></p>
        <p>This link will expire in 24 hours.</p>
        """
        
        await mail_service.send_email(
            to_email=email,
            subject="Password Reset Request",
            html_content=html_content
        )
        
        return True
