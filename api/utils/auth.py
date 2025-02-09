from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from models.user import User
from services.user_service import UserService
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from utils.security import decode_access_token
from db.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    user_id = decode_access_token(token)
    
    # Check if user_id is a valid integer
    if not isinstance(user_id, int):
        raise credentials_exception
        
    user_service = UserService(db)
    user = await user_service.get_user(user_id)
    if user is None:
        raise credentials_exception
        
    return user 