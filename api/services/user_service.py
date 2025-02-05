from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from models.user import UserCreate, User, UserInDB
from db.models import UserDB
from utils.security import get_password_hash
from datetime import datetime

class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    def _map_to_user_in_db(self, db_user: UserDB) -> UserInDB:
        return UserInDB(
            id=db_user.id,
            email=db_user.email,
            full_name=db_user.full_name,
            is_active=db_user.is_active,
            hashed_password=db_user.hashed_password,
            reset_token=db_user.reset_token,
            reset_token_expires=db_user.reset_token_expires
        )

    def _map_to_user(self, db_user: UserDB) -> User:
        return User(
            id=db_user.id,
            email=db_user.email,
            full_name=db_user.full_name,
            is_active=db_user.is_active
        )

    async def create_user(self, user: UserCreate) -> User:
        # Create user in database
        hashed_password = get_password_hash(user.password)
        db_user = UserDB(
            email=user.email,
            full_name=user.full_name,
            hashed_password=hashed_password
        )
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        
        # Convert to Pydantic model and return
        return self._map_to_user(db_user)

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