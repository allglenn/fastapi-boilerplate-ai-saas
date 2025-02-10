from sqlalchemy import Boolean, Column, Integer, String, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

class UserRole(enum.Enum):
    ADMIN = "ADMIN"
    CLIENT = "CLIENT"

class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    reset_token = Column(String, nullable=True)
    reset_token_expires = Column(DateTime, nullable=True)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.CLIENT)

class BlacklistedToken(Base):
    __tablename__ = "blacklisted_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True)
    expires_at = Column(DateTime) 
