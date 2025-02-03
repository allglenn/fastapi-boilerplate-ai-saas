from typing import Any
import jwt
from datetime import datetime, timedelta
from config import settings

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")

def validate_email(email: str) -> bool:
    """Validate email format"""
    # Add email validation logic
    return "@" in email 