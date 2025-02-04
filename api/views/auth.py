from fastapi import APIRouter, Depends, Security
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from models.auth import Token, LoginRequest
from models.user import User
from controllers.auth import AuthController
from services.auth_service import AuthService
from db.database import get_db

router = APIRouter(prefix="/auth", tags=["authentication"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    login_request = LoginRequest(
        email=form_data.username,
        password=form_data.password
    )
    return await AuthController.login(login_request, db)

@router.post("/login", response_model=Token)
async def login(
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    return await AuthController.login(login_data, db)

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    auth_service = AuthService(db)
    return await auth_service.get_current_user(token)

@router.post("/logout")
async def logout(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    return await AuthController.logout(token, db) 

@router.get("/refresh", response_model=Token)
async def refresh_token(
    token: str = Depends(oauth2_scheme),
     db: AsyncSession = Depends(get_db)
    ):
    return await AuthController.refresh_token(token, db) 