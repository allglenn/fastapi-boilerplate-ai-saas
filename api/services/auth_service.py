from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from models.auth import Token, TokenData
from models.user import User, UserInDB
from services.user_service import UserService
from services.token_blacklist import TokenBlacklistService
from utils.security import verify_password, get_password_hash
from config import settings
from models.user import User
import secrets
from services.mail_service import MailService
from sqlalchemy import update
from db.models import UserDB


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
        
        # Store reset token in database using the new method
        await self.user_service.update_user_reset_token(
            email=email,
            reset_token=reset_token,
            expires=expiration
        )

        # Send email
        mail_service = MailService()
        reset_link = f"{settings.DOMAIN_NAME}/reset-password?token={reset_token}"
        html_content = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2 style="color: #333; text-align: center;">{settings.APP_NAME} - Password Reset</h2>
            
            <p>Hello,</p>
            
            <p>We received a request to reset your password for your {settings.APP_NAME} account. 
            If you didn't make this request, you can safely ignore this email.</p>
            
            <p>To reset your password, click the button below. This link will expire in 24 hours:</p>
            
            <div style="text-align: center; margin: 30px 0;">
                <a href="{reset_link}" 
                   style="background-color: #007bff; 
                          color: white; 
                          padding: 12px 24px; 
                          text-decoration: none; 
                          border-radius: 4px;
                          display: inline-block;">
                    Reset Your Password
                </a>
            </div>
            
            <p>Or copy and paste this link into your browser:</p>
            <p style="word-break: break-all; color: #006699;">{reset_link}</p>
            
            <p>For security reasons, this password reset link will expire in 24 hours. 
            After that, you'll need to submit a new password reset request.</p>
            
            <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
            
            <p style="color: #666; font-size: 0.9em;">
                If you didn't request a password reset, please ignore this email or contact support 
                if you have concerns about your account security.
            </p>
            
            <p style="color: #666; font-size: 0.9em;">
                Best regards,<br>
                The {settings.APP_NAME} Team
            </p>
        </div>
        """
        
        await mail_service.send_email(
            to_email=email,
            subject=f"{settings.APP_NAME} - Password Reset Request",
            html_content=html_content
        )
        
        return True

    async def confirm_password_reset(self, token: str, new_password: str) -> bool:
        """Confirm password reset and update the user's password."""
        user = await self.user_service.get_user_by_reset_token(token)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired password reset token"
            )
            
        # Check if token is expired
        if user.reset_token_expires < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password reset token has expired"
            )
            
        # Update password and clear reset token
        query = (
            update(UserDB)
            .where(UserDB.reset_token == token)
            .values(
                hashed_password=get_password_hash(new_password),
                reset_token=None,
                reset_token_expires=None
            )
        )
        await self.db.execute(query)
        await self.db.commit()
        
        return True
