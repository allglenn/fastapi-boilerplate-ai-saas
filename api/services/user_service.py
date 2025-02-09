from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from models.user import UserCreate, User, UserInDB
from db.models import UserDB
from utils.security import get_password_hash
from datetime import datetime
from models.user import UserUpdate
from services.mail_service import MailService
import os
from string import Template
from config import settings
from db.models import UserRole
from fastapi import HTTPException

class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.mail_service = MailService()

    def _map_to_user_in_db(self, db_user: UserDB) -> UserInDB:
        return UserInDB(
            id=db_user.id,
            email=db_user.email,
            full_name=db_user.full_name,
            is_active=db_user.is_active,
            hashed_password=db_user.hashed_password,
            reset_token=db_user.reset_token,
            reset_token_expires=db_user.reset_token_expires,
            role=db_user.role
        )

    def _map_to_user(self, db_user: UserDB) -> User:
        return User(
            id=db_user.id,
            email=db_user.email,
            full_name=db_user.full_name,
            is_active=db_user.is_active,
            role=db_user.role
        )

    async def _send_welcome_email(self, user: User) -> None:
        # Read the email template
        template_path = os.path.join('email-templates', 'auth', 'new_account.html')
        with open(template_path, 'r') as file:
            template = Template(file.read())

        # Format the template with user data
        html_content = template.safe_substitute(
            app_name=settings.APP_NAME,
            full_name=user.full_name,
            email=user.email,
            login_url=f"{settings.DOMAIN_NAME}/login"
        )

        # Send the welcome email
        await self.mail_service.send_email(
            to_email=user.email,
            subject=f"Welcome to {settings.APP_NAME}!",
            html_content=html_content
        )

    async def create_user(self, user: UserCreate) -> User:
        # check if role is admin (remove this check when admin creation is implemented)
        if user.role == UserRole.ADMIN:
            raise HTTPException(status_code=400, detail="Admin role is not allowed to be created by this endpoint")
        # Create user in database
        hashed_password = get_password_hash(user.password)
        db_user = UserDB(
            email=user.email,
            full_name=user.full_name,
            hashed_password=hashed_password,
            role=user.role
        )
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        
        # Convert to Pydantic model
        created_user = self._map_to_user(db_user)
        
        # Send welcome email
        await self._send_welcome_email(created_user)
        
        return created_user

    async def get_user(self, user_id: int) -> User | None:
        query = select(UserDB).where(UserDB.id == user_id)
        result = await self.db.execute(query)
        db_user = result.scalar_one_or_none()
        
        if db_user is None:
            return None
            
        return self._map_to_user(db_user)

    async def get_user_by_email(self, email: str) -> UserInDB | None:
        query = select(UserDB).where(UserDB.email == email)
        result = await self.db.execute(query)
        db_user = result.scalar_one_or_none()
        
        if db_user is None:
            return None
            
        return self._map_to_user_in_db(db_user)

    async def delete_user(self, user_id: int) -> None:
        query = delete(UserDB).where(UserDB.id == user_id)
        await self.db.execute(query)
        await self.db.commit()

    async def update_user_reset_token(self, email: str, reset_token: str, expires: datetime) -> None:
        query = (
            update(UserDB)
            .where(UserDB.email == email)
            .values(reset_token=reset_token, reset_token_expires=expires)
        )
        await self.db.execute(query)
        await self.db.commit()

    async def get_user_by_reset_token(self, reset_token: str) -> UserInDB | None:
        query = select(UserDB).where(UserDB.reset_token == reset_token)
        result = await self.db.execute(query)
        db_user = result.scalar_one_or_none()
        
        if db_user is None:
            return None
            
        return self._map_to_user_in_db(db_user)
    
    async def update_user(self, user_id: int, user_data: UserUpdate) -> User:
        query = (
            update(UserDB)
            .where(UserDB.id == user_id)
            .values(**user_data.model_dump(exclude_none=True))
        )
        await self.db.execute(query)
        await self.db.commit()
        db_user = await self.get_user(user_id)  
        return self._map_to_user(db_user)

    async def get_latest_users(self, limit: int = 100) -> list[User]:
        query = (
            select(UserDB)
            .order_by(UserDB.id.desc())
            .limit(limit)
        )
        result = await self.db.execute(query)
        users = result.scalars().all()
        return [self._map_to_user(user) for user in users]