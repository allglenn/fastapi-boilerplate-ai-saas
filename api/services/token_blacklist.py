from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db.models import BlacklistedToken
from jose import jwt
from config import settings

class TokenBlacklistService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def blacklist_token(self, token: str) -> None:
        try:
            # Decode token to get expiry
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            expires_at = datetime.fromtimestamp(payload['exp'])
            
            # Add token to blacklist
            db_token = BlacklistedToken(
                token=token,
                expires_at=expires_at
            )
            self.db.add(db_token)
            await self.db.commit()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid token"
            )

    async def is_token_blacklisted(self, token: str) -> bool:
        query = select(BlacklistedToken).where(BlacklistedToken.token == token)
        result = await self.db.execute(query)
        return result.scalar_one_or_none() is not None

    async def cleanup_expired_tokens(self) -> None:
        """Remove expired tokens from blacklist"""
        now = datetime.utcnow()
        await self.db.execute(
            BlacklistedToken.__table__.delete().where(
                BlacklistedToken.expires_at < now
            )
        )
        await self.db.commit() 