from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from controllers.user import UserController, router as user_router
from models.user import User, UserCreate, UserUpdate
from db.database import get_db
from views.auth import get_current_user
from typing import List
from db.models import UserRole
from services.user_service import UserService
from fastapi import Depends

# Create router with prefix
router = APIRouter(prefix="/users", tags=["users"])

# Mount the controller router first (for /list endpoint)
router.include_router(user_router)

@router.get("/list", response_model=List[User])
async def get_users(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> List[User]:
    return await UserController.get_users_list(current_user, db)

@router.post("", response_model=User)
async def create_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
) -> User:
    return await UserController.create_user(user_data, db)

@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user 

@router.get("/{user_id}", response_model=User)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
) -> User:
    return await UserController.get_user(user_id, db)

@router.put("/{user_id}", response_model=User)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: AsyncSession = Depends(get_db)
) -> User:
    return await UserController.update_user(user_id, user_data, db)

@router.delete("/{user_id}", status_code=204)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
) -> None:
    return await UserController.delete_user(user_id, db)
