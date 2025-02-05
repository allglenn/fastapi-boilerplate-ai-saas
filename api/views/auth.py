from fastapi import APIRouter, Depends, Security, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from models.auth import Token, LoginRequest, PasswordResetRequest, PasswordResetConfirm
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

@router.post("/password-reset/request")
async def request_password_reset(
    reset_request: PasswordResetRequest,
    db: AsyncSession = Depends(get_db)
):
    auth_service = AuthService(db)
    success = await auth_service.create_password_reset_token(reset_request.email)
    
    # Always return success to prevent email enumeration
    return {"message": "If the email exists, a password reset link will be sent."} 

@router.post("/password-reset/confirm")
async def confirm_password_reset(
    reset_data: PasswordResetConfirm,
    db: AsyncSession = Depends(get_db)
):
    """Confirm password reset and update the password."""
    auth_service = AuthService(db)
    await auth_service.confirm_password_reset(
        token=reset_data.token,
        new_password=reset_data.new_password
    )
    return {"message": "Password has been successfully reset"} 
